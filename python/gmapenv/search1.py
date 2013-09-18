#!/usr/bin/env python
# Foundations of Python Network Programming - Chapter 1 - search1.py
# Googlemaps API deprecated#
from googlemaps import GoogleMaps
# this will currently fail, needs api key
# gmaps = GoogleMaps(api_key)
gmaps = GoogleMaps()
address = '207 N. Defiance St, Archbold, OH'
print gmaps.address_to_latlng(address)
