#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================
Copyright (c) 2018, EPOS Project
================================
---
Three ways to call the FDSN-event's web service.
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

# Download and parse (txt)
url = "http://www.seismicportal.eu/fdsnws/event/1/query?eventid={unid}&format=text".format(unid=main_event['unid'])
res = geturl(url)
dataev = parsecsv(res['content'])
print("---parse-txt---\n{0}\n".format(dataev))

# Download and parse (json)
url = "http://www.seismicportal.eu/fdsnws/event/1/query?eventid={unid}&format=json".format(unid=main_event['unid'])
res = geturl(url)
dataev = parsejson(res['content'])
eqinfo = dataev['properties']
print("---parse-json---\n{0}\n".format(eqinfo))

# Download and parse (xml)
url = "http://www.seismicportal.eu/fdsnws/event/1/query?eventid={unid}&format=xml".format(unid=main_event['unid'])
dataev = parsexml(url)
print("---parse-xml---\n{0}".format(dataev))
