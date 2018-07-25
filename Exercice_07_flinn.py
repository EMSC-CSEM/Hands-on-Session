#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================
Copyright (c) 2018, EPOS Project
================================
---
Fetch Flinn-Endghal  
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

# Step 1/2 -- Download and parse (json)
url = "http://www.seismicportal.eu/fdsnws/event/1/query?eventid={unid}&format=json".format(unid=main_event['unid'])
res = geturl(url)
dataev = parsejson(res['content'])
eqinfo = dataev['properties']
#print("---parse-json---\n{0}\n".format(eqinfo))

# Step 2/2 -- Fetch Flinn-Endghal
url = "http://www.seismicportal.eu/fe_regions_ws/query?format=json&lat={lat}&lon={lon}"
res = geturl(url.format(**eqinfo))
print parsejson(res['content'])
