import json
import networkx as nx
from networkx.readwrite import json_graph
import httplib2

baseUrl = 'http://localhost:8080/controller/nb/v2/'
containerName = 'default/'

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')

# Get all the edges/links
resp, content = h.request(baseUrl + 'topology/' + containerName, "GET")
edgeProperties = json.loads(content)
odlEdges = edgeProperties['edgeProperties']

# Get all the nodes/switches
resp, content = h.request(baseUrl + 'switchmanager/' + containerName + 'nodes/', "GET")
nodeProperties = json.loads(content)
odlNodes = nodeProperties['nodeProperties']

# Get all the actie hosts
resp, content = h.request(baseUrl + 'hosttracker/' + containerName + 'hosts/active', "GET")
hostProperties = json.loads(content)
hosts = hostProperties["hostConfig"]

# Initialize the graph
graph = nx.Graph()

#  Put switches in the graph
for node in odlNodes:
  graph.add_node(node['node']['id'])

#  Put all the edges between switches
for edge in odlEdges:
  e = (edge['edge']['headNodeConnector']['node']['id'], edge['edge']['tailNodeConnector']['node']['id'])
  graph.add_edge(*e)

#  Put hosts in the graph and the relevant edges
for host in hosts:
  graph.add_node(host['networkAddress'])
  e = (host['networkAddress'], host['nodeId'])
  graph.add_edge(*e)

# Print out graph info as a sanity check
print "Number of nodes add in the graph:", graph.number_of_nodes()
print "Nodes are:", graph.nodes()

# write json formatted data to use in visualization
d = json_graph.node_link_data(graph)
json.dump(d, open('topo.json','w'))
print('Wrote node-link JSON data')
