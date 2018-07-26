#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================
Copyright (c) 2018, EPOS Project
================================
---
Fetch Testimonies 
unid = '20170919_0000091'
"""

# -------------------------------------
# Main functions used in the EUrythmics
# -------------------------------------
# Func-Download
import requests
def geturl(url):
    res = requests.get(url, timeout=15)
    return {'status': res.status_code,
            'content': res.text}

# Func-Parse (txt)
import csv
from io import StringIO
def parsecsv(txt, usedict=False):
    if usedict:
        parser = csv.DictReader(StringIO(txt), delimiter='|')
    else:
        parser = csv.reader(StringIO(txt), delimiter='|')        
    return [line for line in parser]

# Func-Parse (json)
import json
def parsejson(txt):
    return json.loads(txt)

# Func-Parse (xml)
from obspy import read_events
def parsexml(url):
   return read_events(url)
# ===================================

main_event = {'unid':'20170919_0000091'}

# Step 1 => How many testimonies? 
url = "http://www.seismicportal.eu/testimonies-ws/api/search?eventid={unid}&format=json"
tdata = parsejson(geturl(url.format(**main_event))['content'])
print json.dumps(tdata, indent=4, sort_keys=True)
print '=> Number of Testimonies:', tdata[0]['ev_nbtestimonies']

# Step 2 => Recover intensity data points
import  zipfile
from io import BytesIO
url = "http://www.seismicportal.eu/testimonies-ws/api/search?unids=[{unid}]&includeTestimonies=true"
r = requests.get(url.format(**main_event), stream=True)
z = zipfile.ZipFile(BytesIO(r.content)) # print 'Downloaded result:', z.namelist()

filename = "{unid}.txt".format(**main_event)
data = z.read(filename)
data = data.split('\n')

# -- Header
print '\n'*2 + 'Longitude | Latitude | Intensity (raw) | Intensity (corrected)' 

# -- Print the first 10 Intensity data point  
for ii in range(10):
   print data[4+ii:4+(ii+1)][0]
print '(...)' 
