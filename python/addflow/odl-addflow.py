import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2

class Node:
  def __init__(self, **entries):
    self.__dict__.update(entries)

baseUrl = 'http://10.55.17.20:8080/controller/nb/v2/'
containerName = 'default/'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

def post_dict(h, url, d):
  resp, content = h.request(
      uri = url,
      method = 'POST',
      headers={'Content-Type' : 'application/json'},
      body=json.dumps(d),
      )
  print resp
  print content

# Get all the edges/links
resp, content = h.request(baseUrl + 'topology/' + containerName, "GET")
edgeProperties = json.loads(content)
odlEdges = edgeProperties['edgeProperties']
print json.dumps(odlEdges, indent=2)

# Get all the nodes/switches
resp, content = h.request(baseUrl + 'switch/' + containerName + 'nodes/', "GET")
nodeProperties = json.loads(content)
odlNodes = nodeProperties['nodeProperties']
#print odlNodes
#for node in odlNodes:
  #print json.dumps(node, indent=2)
#graph.add_nodes_from(odlNodes)

# Put nodes and edges into a graph
graph = nx.Graph()
for node in odlNodes:
  #n = Node(**node)
  #graph.add_node(n)
  graph.add_node(node['node']['@id'])
for edge in odlEdges:
  e = (edge['edge']['headNodeConnector']['node']['@id'], edge['edge']['tailNodeConnector']['node']['@id'])
  graph.add_edge(*e)
# Print out graph info as a sanity check
print graph.number_of_nodes()
print graph.nodes()
#print json.dumps(odlNodes, indent = 2)
# These JSON dumps were handy when trying to parse the responses 
#print json.dumps(topo[0], indent = 2)
print "shortest path from 3 to 7" 
shortest_path = nx.shortest_path(graph, "00:00:00:00:00:00:00:03", "00:00:00:00:00:00:00:07")
print shortest_path
for edge in odlEdges:
  if edge['edge']['headNodeConnector']['node']['@id'] == shortest_path[0] and edge['edge']['tailNodeConnector']['node']['@id'] == shortest_path[1]:
    print json.dumps(edge, indent=2)
    print "ingress port "
    print "OUTPUT Port = "
    print edge['edge']['headNodeConnector']['@id']
flowName = "test2/"
switchId = "OF/00:00:00:00:00:00:00:07/"
newFlow = {"installInHw":"false","name":"test2","node":{"@id":"00:00:00:00:00:00:00:07","@type":"OF"},"ingressPort":"1","priority":"500","etherType":"0x800","nwSrc":"10.0.0.7","nwDst":"10.0.0.3","actions":"OUTPUT=2"}
print "*** dump new flow***"
print json.dumps(newFlow)
postUrl = baseUrl + 'flow/' + containerName + switchId + flowName
print postUrl
post_dict(h, postUrl, newFlow)

# write json formatted data to use in visualization
d = json_graph.node_link_data(graph)
json.dump(d, open('topo.json','w'))
print('Wrote node-link JSON data')


