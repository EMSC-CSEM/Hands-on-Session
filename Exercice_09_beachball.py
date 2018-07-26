#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================
Copyright (c) 2018, EPOS Project
================================
---
Fetch Moment Tensors 
+ plot Beachball
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


from obspy.imaging.beachball import beachball

#url= "http://vigogne.emsc-csem.org/mtws/api/search\
#?source_catalog=USGS&eventid=20170919_0000091&format=text"

url = "http://www.seismicportal.eu/mtws/api/search\
?source_catalog=USGS&eventid=20170919_0000091&format=text"

mt = parsecsv(geturl(url)['content'], usedict=True)[0] #we get a list with only one element.

t = map(float, [mt['mt_mrr'], mt['mt_mtt'], mt['mt_mpp'], mt['mt_mrt'], mt['mt_mrp'], mt['mt_mtp']])

print '='*46 
print "{mt_source_catalog} Solution, Strike: {mt_strike_1}, Dip: {mt_dip_1}, Rake: {mt_rake_1}".format(**mt)
print '='*46

beachball(t, width=200);


