#!/usr/bin/env python
import requests
import json
from requests.auth import HTTPBasicAuth

# Global variables
serverIP = '10.55.17.20'
port = '8080'
container = 'default'
user = 'admin'
password = 'admin'

# given a list of subnets and a subnet to find, will return the subnet if found
# or None if not found
def find_subnet(subnets, subnetName):
    allSubnets = '/controller/nb/v2/subnet/' + container + '/subnet/all'
    url = 'http://' + serverIP + ':' + port + allSubnets
    for subnet in subnets:
        if subnet['subnet'] == subnetName:
            return subnet
    return None

# Similiar to above, rewriting to use API
def find_subnet2(subnet):
    findSubnetPath = '/controller/nb/v2/subnet/' + container + '/' + subnetName
    url = 'http://' + serverIP + ':' + port + findSubnetPath
    try:
        r = requests.post(url, auth=(user, password))
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print e
        return None
    else:
        print "subnet found"
        return r.json()

# Finds all the subnets that are in a list
# Just an excuse to practice list comprehensions
def find_subnets(subnetList):
    path = '/controller/nb/v2/subnet/' + container + '/subnet/all'
    url = 'http://' + serverIP + ':' + port + path
    try:
        r = requests.post(url, auth=(user, password))
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print e
        return None
    else:
        found = [x for x in r.json()[ 'subnetConfig' ] if x['subnet'] in subnetList]
        return found

# Given a name and subnet, will add the subnet to the controller
# Will return the subnet added in JSON format if successful
# Otherwise, will return None

def add_subnet(name, subnet):
    url = 'http://10.55.17.20:8080/controller/nb/v2/subnet/' + container + '/subnet/' + name
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    payload = {
        "name" : name,
        "subnet" : subnet
            }
    try:
        r = requests.post(url, data=json.dumps(payload), headers = headers, auth=(user, password))
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print e
        return None
    else:
        print "subnet added"
        return json.dumps(payload)

allSubnets = '/controller/nb/v2/subnet/' + container + '/subnet/all'
url = 'http://' + serverIP + ':' + port + allSubnets
errorcodes = {
    400: 'Invalid data',
    401: 'User not authorized',
    409: 'Name conflict',
    404: 'Container name not found',
    500: 'Internal error',
    503: 'Service unavailable'
    }

subnetquery = '10.2.2.254/24'
try:
    r = requests.get(url, auth=(user, password))
    r.raise_for_status()
except requests.exceptions.HTTPError as e:
    print e
    print "Reason : %s" % errorcodes[r.status_code]
else:
    # No errors loading URL
    result = find_subnet(r.json()['subnetConfig'], subnetquery)
    print result

add_subnet('test4', '3.31.54.254/24')
