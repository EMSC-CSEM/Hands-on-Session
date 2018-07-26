#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================
Copyright (c) 2018, EPOS Project
================================
---
Fetch EventID 
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

url = "http://www.seismicportal.eu/eventid/api/convert?source_id={id}&source_catalog={source}&out_catalog={out}&format=text"
res = geturl(url.format(id=main_event['unid'], source='UNID', out='all'))
iddata = parsecsv(res['content'], usedict=True)

for l in iddata:
    print "\n* Institute {#catalog:5}, ID: {eventid}\n   url: {url}".format(**l)

