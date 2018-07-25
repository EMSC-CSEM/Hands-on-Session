#!/bin/bash

#================================
#Copyright (c) 2018, EPOS Project
#================================
url="http://www.seismicportal.eu/fdsnws/event/1/query?start=2017-09-01&end=2017-11-01&format=text&minmag=6.5"
wget -O result_Exercice_03.txt ${url}
o=`cat result_Exercice_03.txt`
echo "$o"
