import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2

baseUrl = 'http://10.55.17.20:8080/controller/nb/v2'
containerName = 'default'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
def build_url(baseUrl, service, containerName):
  postUrl = '/'.join([baseUrl, service, containerName])
  print postUrl
  return postUrl

def build_flow_url(baseUrl, containerName, switchType, switchId, flowName):
  postUrl = build_url(baseUrl, 'flow', containerName) + '/'.join(['', switchType, switchId, flowName])
  print postUrl
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
#print json.dumps(odlEdges, indent=2)

# Get all the nodes/switches
resp, content = h.request(build_url(baseUrl, 'switch', containerName) + '/nodes/', "GET")
nodeProperties = json.loads(content)
odlNodes = nodeProperties['nodeProperties']

# Put nodes and edges into a graph
graph = nx.Graph()
for node in odlNodes:
  # Might replace this with the actual node object to make stuff easier later
  graph.add_node(node['node']['@id'], nodeType=node['node']['@type'])
for edge in odlEdges:
  e = (edge['edge']['headNodeConnector']['node']['@id'], edge['edge']['tailNodeConnector']['node']['@id'])
  graph.add_edge(*e)

# Print out graph info as a sanity check
print "shortest path from 3 to 7" 
shortest_path = nx.shortest_path(graph, "00:00:00:00:00:00:00:03", "00:00:00:00:00:00:00:07")
print shortest_path
newFlow = {}
srcIP = "10.0.0.7"
dstIP = "10.0.0.3"
etherTypeIP = "0x800"
defaultPriority = "500"
# Iterate for the 'intermediate' switches, not connected to a host port
for i, node in enumerate(shortest_path[1:-1]):
  newflow = {}
  flowName = "test" + str(i)
  ingressEdge = next(edge for edge in odlEdges if edge['edge']['headNodeConnector']['node']['@id'] == shortest_path[i] and edge['edge']['tailNodeConnector']['node']['@id'] == node)
  egressEdge = next(edge for edge in odlEdges if edge['edge']['headNodeConnector']['node']['@id'] == node and edge['edge']['tailNodeConnector']['node']['@id'] == shortest_path[i+2])

  ingressPort = ingressEdge['edge']['tailNodeConnector']['@id']
  egressPort = egressEdge['edge']['headNodeConnector']['@id']
  switchType = egressEdge['edge']['headNodeConnector']['node']['@type']
  switchId = node
  newFlow.update({"installInHw":"false", "name":flowName})
  newFlow.update({"node":ingressEdge['edge']['tailNodeConnector']['node']})
  newFlow.update({"ingressPort":ingressPort, "priority":defaultPriority, "etherType":etherTypeIP, "nwSrc":srcIP, "nwDst":dstIP, "actions":"OUTPUT=" + egressPort})
#newFlow = {"installInHw":"false","name":"test2","node":{"@id":"00:00:00:00:00:00:00:07","@type":"OF"},"ingressPort":"1","priority":"500","etherType":"0x800","nwSrc":"10.0.0.7","nwDst":"10.0.0.3","actions":"OUTPUT=2"}
  print "*** dump new flow***"
  print newFlow
  #print json.dumps(newFlow)
  postUrl = build_flow_url(baseUrl, 'default', switchType, switchId, flowName)
  resp, content = post_dict(h, postUrl, newFlow)

