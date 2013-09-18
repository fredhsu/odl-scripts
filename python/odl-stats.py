import httplib2
import json

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
# Updated 8 SEP 2013 to reflect new rest api, changed from /flowstats to /flow
resp, content = h.request('http://10.55.17.20:8080/controller/nb/v2/statistics/default/flow', "GET")
allFlowStats = json.loads(content)
flowStats = allFlowStats['flowStatistics']
# These JSON dumps were handy when trying to parse the responses 
#print json.dumps(flowStats[0]['flowStat'][1], indent = 2)
#print json.dumps(flowStats[4], indent = 2)
for fs in flowStats:
	print "\nSwitch ID : " + fs['node']['@id']
	print '{0:8} {1:8} {2:5} {3:15}'.format('Count', 'Action', 'Port', 'DestIP')
	for aFlow in fs['flowStat']:
		count = aFlow['packetCount']
		actions = aFlow['flow']['actions'] 
		actionType = ''
		actionPort = ''
		#print actions
		if(type(actions) == type(list())):
			actionType = actions[1]['@type']
			actionPort = actions[1]['port']['@id']
		else:
			actionType = actions['@type']
			actionPort = actions['port']['@id']
		dst = aFlow['flow']['match']['matchField'][0]['value']
		print '{0:8} {1:8} {2:5} {3:15}'.format(count, actionType, actionPort, dst)
