#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

root = None

for line in sys.stdin:
    line = line.strip()
    root = ET.fromstring(line)
    #if question
    if root.attrib['PostTypeId'] == "1" and ('AcceptedAnswerId' in root.attrib):
        print "{0}\t0".format(root.attrib['AcceptedAnswerId']) 
        #emit 'acceptedID, 0' and hope they indexed form 1
    #if answer
    elif 'OwnerUserId' in root.attrib:
        print "{0}\t{1}".format(root.attrib['Id'], root.attrib['OwnerUserId'])
        #emit 'acceptedID, ownerID'