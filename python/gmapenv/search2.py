#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 1 - search2.py
#
import urllib, urllib2
try:
    import json
except ImportError:  # for Python 2.5
    import simplejson as json

params = {'q': '207 N. Defiance St, Archbold, OH',
        'output': 'json', 'oe': 'utf8'}
params = {'address': '4479 Laird Cir, Santa Clara, CA', 'sensor': 'false'}
#url = 'http://maps.google.com/maps/geo?' + urllib.urlencode(params)
url = 'http://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(params)
print url

rawreply = urllib2.urlopen(url).read()
reply = json.loads(rawreply)
print reply['results'][0]['geometry']['location']
#print reply['Placemark'][0]['Point']['coordinates'][:-1]
