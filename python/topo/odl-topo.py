import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2

class Node:
  def __init__(self, **entries):
    self.__dict__.update(entries)

baseUrl = 'http://localhost:8080/controller/nb/v2/'
containerName = 'default/'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

# Get all the edges/links
resp, content = h.request(baseUrl + 'topology/' + containerName, "GET")
edgeProperties = json.loads(content)
odlEdges = edgeProperties['edgeProperties']

# Get all the nodes/switches
resp, content = h.request(baseUrl + 'switch/' + containerName + 'nodes/', "GET")
nodeProperties = json.loads(content)
odlNodes = nodeProperties['nodeProperties']
#print odlNodes
#for node in odlNodes:
  #print json.dumps(node)
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


# write json formatted data to use in visualization
d = json_graph.node_link_data(graph)
json.dump(d, open('topo.json','w'))
print('Wrote node-link JSON data')


