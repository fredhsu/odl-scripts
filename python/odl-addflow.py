import httplib2
import json

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
resp, content = h.request('http://localhost:8080/controller/nb/v2/topology/default/', "GET")
allTopo = json.loads(content)
topo = allTopo['edgeProperties']
# These JSON dumps were handy when trying to parse the responses 
print topo
print json.dumps(topo[0])
print json.dumps(topo[0]['properties'][1], indent = 2)
print json.dumps(topo[4], indent = 2)
