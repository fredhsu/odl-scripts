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
  return postUrl

def build_flow_url(baseUrl, containerName, switchType, switchId, flowName):
  postUrl = build_url(baseUrl, 'flow', containerName) + '/'.join(['', switchType, switchId, flowName])
  return postUrl

# Get all the flows
resp, content = h.request(build_url(baseUrl, 'flow', containerName), "GET")
flowsList = json.loads(content)
odlFlowConfigs = flowsList['flowConfig']

# Now go and delete them all
for flow in odlFlowConfigs:
  nodeType = flow['node']['@type']
  nodeId = flow['node']['@id']
  name = flow['name']
  deleteUrl = build_url(baseUrl, 'flow', containerName) + \
    '/'.join(['', nodeType, nodeId, name])
  h.request(deleteUrl, "DELETE")
