#! /usr/bin/python

import httplib
try:
    import json
except ImportError: 
    import simplejson as json

path = ('/maps/api/geocode/json??q=207+N.+Defiance+St%2C+Archbold%2C+OH')

connection = httplib.HTTPConnection('maps.googleapis.com')
connection.request('GET', path)
rawreply = connection.getresponse().read()

reply = json.loads(rawreply)
print reply
