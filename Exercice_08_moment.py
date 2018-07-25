#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================
Copyright (c) 2018, EPOS Project
================================
---
Fetch Moment Tensors  
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

# Step 1/3 -- Download and parse (json)
url = "http://www.seismicportal.eu/fdsnws/event/1/query?eventid={unid}&format=json".format(unid=main_event['unid'])
res = geturl(url)
dataev = parsejson(res['content'])
eqinfo = dataev['properties']

# Step 2/3 -- Full Contents
url = "http://www.seismicportal.eu/mtws/api/search?format=text&eventid={unid}"
res = geturl(url.format(unid=main_event['unid']))
print '\n' + '** Full MT Contents **'
print res['content'][:1000]

# Step 3/3 -- Filtered Information
mt_data = parsecsv(res['content'], usedict=True)
print '\n' + '** Filtered Information **'
for mt in mt_data:
    print "Mt from {mt_source_catalog:10}, Strike: {mt_strike_1}, Dip: {mt_dip_1}, Rake: {mt_rake_1}".format(**mt)
print '\n'
