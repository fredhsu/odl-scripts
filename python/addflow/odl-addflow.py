import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2

# If I want to create node objects, but may not need to
class Node(object):
  def __init__(self, nodeId, nodeType):
    self.nodeId = nodeId
    self.nodeType = nodeType

def node_decoder(obj):
  if obj['__type__'] == 'Node':
    return Node(obj['@id'], obj['@type'])
  return obj

baseUrl = 'http://10.55.17.20:8080/controller/nb/v2'
containerName = 'default'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
def push_path(path, odlEdges, srcIP, dstIP, baseUrl):
  for i, node in enumerate(path[1:-1]):
    flowName = "fromIP" + srcIP[-1:] + "Po" + str(i)
    ingressEdge = next(edge for edge in odlEdges if edge['edge']['headNodeConnector']['node']['@id'] == shortest_path[i] and edge['edge']['tailNodeConnector']['node']['@id'] == node)
    egressEdge = next(edge for edge in odlEdges if edge['edge']['headNodeConnector']['node']['@id'] == node and edge['edge']['tailNodeConnector']['node']['@id'] == shortest_path[i+2])
    print "***"
    newFlow = build_flow_entry(flowName, ingressEdge, egressEdge, node, srcIP, dstIP)
    print json.dumps(newFlow)
    switchType = newFlow['node']['@type']
    postUrl = build_flow_url(baseUrl, 'default', switchType, node, flowName)
    # post the flow to the controller
    resp, content = post_dict(h, postUrl, newFlow)
    print resp

def build_flow_entry(flowName, ingressEdge, egressEdge, node, srcIP, dstIP):
  # *** Example flow: newFlow = {"installInHw":"false","name":"test2","node":{"@id":"00:00:00:00:00:00:00:07","@type":"OF"},"ingressPort":"1","priority":"500","etherType":"0x800","nwSrc":"10.0.0.7","nwDst":"10.0.0.3","actions":"OUTPUT=2"}
  #etherTypeIP = "0x800"
  defaultPriority = "500"
  newFlow = {"installInHw":"false"}
  ingressPort = ingressEdge['edge']['tailNodeConnector']['@id']
  egressPort = egressEdge['edge']['headNodeConnector']['@id']
  switchType = egressEdge['edge']['headNodeConnector']['node']['@type']
  newFlow.update({"name":flowName})
  newFlow.update({"node":ingressEdge['edge']['tailNodeConnector']['node']})
  newFlow.update({"ingressPort":ingressPort, "priority":defaultPriority, "nwSrc":srcIP, "nwDst":dstIP, "actions":"OUTPUT=" + egressPort})
  return newFlow

def build_url(baseUrl, service, containerName):
  postUrl = '/'.join([baseUrl, service, containerName])
  return postUrl

def build_flow_url(baseUrl, containerName, switchType, switchId, flowName):
  postUrl = build_url(baseUrl, 'flow', containerName) + '/'.join(['', switchType, switchId, flowName])
  return postUrl

def post_dict(h, url, d):
  resp, content = h.request(
      uri = url,
      method = 'POST',
      headers={'Content-Type' : 'application/json'},
      body=json.dumps(d),
      )
  return resp, content

# Get all the edges/links
resp, content = h.request(build_url(baseUrl, 'topology', containerName), "GET")
edgeProperties = json.loads(content)
odlEdges = edgeProperties['edgeProperties']
# Get all the nodes/switches
resp, content = h.request(build_url(baseUrl, 'switch', containerName) + '/nodes/', "GET")
nodeProperties = json.loads(content)
odlNodes = nodeProperties['nodeProperties']

# Put nodes and edges into a graph
graph = nx.Graph()
for node in odlNodes:
  graph.add_node(node['node']['@id'], nodeType=node['node']['@type'])
  # this doesn't work b/c dict is not hashable 
  # graph2.add_node(node['node'])
for edge in odlEdges:
  e = (edge['edge']['headNodeConnector']['node']['@id'], edge['edge']['tailNodeConnector']['node']['@id'])
  graph.add_edge(*e)

# Print out graph info as a sanity check
print "shortest path from 3 to 7" 
shortest_path = nx.shortest_path(graph, "00:00:00:00:00:00:00:03", "00:00:00:00:00:00:00:07")
print shortest_path
srcIP = "10.0.0.1"
dstIP = "10.0.0.8"
# Iterate for the 'intermediate' switches, not connected to a host port
for i, node in enumerate(shortest_path[1:-1]):
  flowName = "test" + str(i)
  ingressEdge = next(edge for edge in odlEdges if edge['edge']['headNodeConnector']['node']['@id'] == shortest_path[i] and edge['edge']['tailNodeConnector']['node']['@id'] == node)
  egressEdge = next(edge for edge in odlEdges if edge['edge']['headNodeConnector']['node']['@id'] == node and edge['edge']['tailNodeConnector']['node']['@id'] == shortest_path[i+2])
  print "*** dump new flow***"
  newFlow = build_flow_entry(flowName, ingressEdge, egressEdge, node, srcIP, dstIP)
  print json.dumps(newFlow)
  switchType = newFlow['node']['@type']
  postUrl = build_flow_url(baseUrl, 'default', switchType, node, flowName)
  # post the flow to the controller
  #resp, content = post_dict(h, postUrl, newFlow)
push_path(shortest_path, odlEdges, srcIP, dstIP, baseUrl)
# Do the same as above but for the reverse direction
shortest_path.reverse()
print shortest_path
push_path(shortest_path, odlEdges, dstIP, srcIP, baseUrl)

# Now we need to add the flows for the hosts

node3FlowFromHost = {"installInHw":"false","name":"node3from","node":{"@id":"00:00:00:00:00:00:00:03","@type":"OF"},"ingressPort":"1","priority":"500","nwSrc":"10.0.0.1","actions":"OUTPUT=3"}
node7FlowFromHost = {"installInHw":"false","name":"node7from","node":{"@id":"00:00:00:00:00:00:00:07","@type":"OF"},"ingressPort":"1","priority":"500","nwSrc":"10.0.0.8","actions":"OUTPUT=3"}
node3FlowToHost = {"installInHw":"false","name":"node3to","node":{"@id":"00:00:00:00:00:00:00:03","@type":"OF"},"ingressPort":"3","priority":"500","nwDst":"10.0.0.1","actions":"OUTPUT=1"}
node7FlowToHost = {"installInHw":"false","name":"node7to","node":{"@id":"00:00:00:00:00:00:00:07","@type":"OF"},"ingressPort":"3","priority":"500","nwDst":"10.0.0.8","actions":"OUTPUT=2"}
postUrl = build_flow_url(baseUrl, 'default', "OF", "00:00:00:00:00:00:00:03", "node3from")
#resp, content = post_dict(h, postUrl, node3FlowFromHost)
#print resp
#print content

