#!/usr/bin/env python
#-*-coding:utf-8-*-
"""
Copyright (c) 2018, EPOS Project
---
Andres.Heinloo@gfz-potsdam.de and,
Aurelien.Dupont@emsc-csem.org
"""

import os, sys
import bson.json_util
from urllib import urlopen

# Moment Tensors rules -- buses
#BUS='http://cerf.emsc-csem.org:80/MTtest_rule0'  # rule "Closest"
BUS='http://cerf.emsc-csem.org:80/MTtest_rule1'  # rule "Faster" 
#BUS='http://cerf.emsc-csem.org:80/MTtest_rule2' # rule "Strongest"
#BUS='http://cerf.emsc-csem.org:80/MTtest_rule3' # rule "Highest"

def utctime():
    ''' UTC timestamp '''
    import time, datetime
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st

print("\nConnecting to {0} and receiving objects:\n".format(BUS))

param = {
    'heartbeat': 10,
    'queue': {
        'SYSTEM_ALERT': {
            'seq': -1
        }
    }
}

ack = bson.BSON(urlopen(BUS + '/open', bson.BSON.encode(param)).read()).decode()
print bson.json_util.dumps(ack, indent=2)

for msg in bson.decode_file_iter(urlopen(BUS + '/stream/' + str(ack['sid']))):

    try:

        QUEUE     = msg['queue']            # Name of the queue....[OK]
        TYPE      = msg['type']             # Queue type...........[OK]
        SENDER    = msg['sender']           # Name of the sender...[OK]
        SEQ       = msg['seq']              # Sequence number......[OK]
        LEVEL     = msg['data']['level']    # Level / action.......[OK]    
        DATA      = msg['data']['text']     # Data exchanged.......[OK]
        FILENAME  = msg['data']['filename'] # Name of the file.....[OK]
        
        if LEVEL=='txt':
            ''' TEXT Mode '''
            print("[{0} UTC] {1}".format(utctime(), DATA))

        elif LEVEL=='img':
            ''' IMG Mode '''
            import base64
            print("Receiving IMG file...[OK]\t <{0}>".format(FILENAME))
            f = open(FILENAME, 'wb')
            f.write(DATA.decode('base64'))
            f.close()

        elif LEVEL=='qml':
            ''' XML Mode '''
            print("Receiving XML file...[OK]\t <{0}>".format(FILENAME))
            f= open(FILENAME, 'w')
            f.write(DATA.encode('utf-8'))
            f.close()

        else:
            pass

    except:
        pass   
