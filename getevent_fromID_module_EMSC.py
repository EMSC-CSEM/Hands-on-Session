#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
================================
Copyright (c) 2018, EPOS Project
================================
Alberto.Michelini@ingv.it &
Aurelien.Dupont@emsc-csem.org
---
Retrieves all scientific figures from EMSC's website.
Input's identifier is EVID or UNID (i.e. Seismic Portal world).
"""

import os, sys
import urllib
import json
import StringIO

def get_event_EMSC(ID):
  ''' Extracts relevant information from EMSC
      ID could be UNID (e.g. 20170203_000010) => Seismic Portal or,
                  EVID (e.g. 564926) => EMSC website. '''

  if (len(ID) > 8):
     ''' [ID] is < UNID >
         Unique identifier used with the Seismic Portal'''
  
     UNID = ID
   
     url_unid   = 'http://www.seismicportal.eu/fdsnws/event/1/query?eventid=' + UNID

     data = urllib.urlopen(url_unid).read() # data are in JSON format 
     DATA = json.loads(data)                # Now JSON is a Python dict

     if 'source_id' in DATA['properties'].keys():
        ''' source_id is EVID '''

        EVID = DATA['properties']['source_id'] # Recover the EVID
  
  elif (len(ID) < 8):
     ''' [ID] is < UNID >
         Event identifier used with the EMSC website '''

     EVID = ID

  # Root path obtained from the EVID
  Id2 = int(int(EVID) / 10000) 
  Id3 = int(int(EVID) / 1000)

  # Build the main path 
  url_images      = 'http://www.emsc-csem.org/Images/EVID/' # e.g. http://www.emsc-csem.org/Images/EVID/57/572/572980/572980.EMMA.jpg
  url_images_evid = "{0}{1}/{2}/{3}/{4}".format(url_images, str(Id2), str(Id3), str(EVID),  str(EVID))

  # Construct the ad hoc URLs from thre main path in order to recover MAPS:
  url_global_map       = "{0}{1}".format(url_images_evid, '.global.jpg')
  url_regional_map     = "{0}{1}".format(url_images_evid, '.regional.jpg') 
  url_local_map        = "{0}{1}".format(url_images_evid, '.local.jpg')
  url_reg_seis_map_dep = "{0}{1}".format(url_images_evid, '.regional.seismicity.depth.jpg') 
  url_reg_seis_map_mag = "{0}{1}".format(url_images_evid, '.regional.seismicity.mag.jpg')
  url_MTs              = "{0}{1}".format(url_images_evid, '.MT.jpg')
  url_EMMA             = "{0}{1}".format(url_images_evid, '.EMMA.jpg')
  url_population       = "{0}{1}".format(url_images_evid, '.population.jpg')
  url_pga              = "{0}{1}".format(url_images_evid, '.pga.jpg')
  url_pgv              = "{0}{1}".format(url_images_evid, '.pgv.jpg')

  # ----------------------------------------------------- 
  # Name of the storage folder where to print MAPS
  # -----------------------------------------------------
  eventdir = os.path.join(os.getcwd(), 'FIG_EVID' + EVID)

  if not os.path.isdir(eventdir):
     ''' Build the folder where to store the MAPS '''
     os.mkdir(eventdir)
  # -----------------------------------------------------

  # Specify the name and the path where to store maps downloaded: 
  global_map       = "{0}/{1}".format(eventdir, 'EMSC_global.jpg')
  regional_map     = "{0}/{1}".format(eventdir, 'EMSC_regional.jpg')  
  local_map        = "{0}/{1}".format(eventdir, 'EMSC_local.jpg') 
  reg_seis_map_dep = "{0}/{1}".format(eventdir, 'EMSC_regional_seismicity_depth.jpg')
  reg_seis_map_mag = "{0}/{1}".format(eventdir, 'EMSC_regional_seismicity_mag.jpg')
  MTs              = "{0}/{1}".format(eventdir, 'EMSC_MT.jpg')
  EMMA             = "{0}/{1}".format(eventdir, 'EMSC_EMMA.jpg')
  population       = "{0}/{1}".format(eventdir, 'EMSC_population.jpg')
  pga              = "{0}/{1}".format(eventdir, 'EMSC_pga.jpg')
  pgv              = "{0}/{1}".format(eventdir, 'EMSC_pgv.jpg')

  # Download images...[RUN]
  urllib.urlretrieve(url_global_map       , global_map)
  urllib.urlretrieve(url_regional_map     , regional_map)
  urllib.urlretrieve(url_local_map        , local_map)
  urllib.urlretrieve(url_reg_seis_map_dep , reg_seis_map_dep)
  urllib.urlretrieve(url_reg_seis_map_mag , reg_seis_map_mag)
  urllib.urlretrieve(url_MTs              , MTs)
  urllib.urlretrieve(url_EMMA             , EMMA)
  urllib.urlretrieve(url_population       , population)
  urllib.urlretrieve(url_pga              , pga)
  urllib.urlretrieve(url_pgv              , pgv)

  Nfile = os.listdir(eventdir)

  print('\n{:-<20}'.format('---'))
  print('{:-^20}'.format('Storage'))
  print("Extracted: {0} files from EMSC website\nMaps are available in local at the following adress:\n{1}".format(len(Nfile), eventdir))
  print('{:-<20}'.format('---'))

if __name__ == '__main__':

  get_event_EMSC(sys.argv[1]) # UNID or EVID
