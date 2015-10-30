#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET

root = None

for line in sys.stdin:
    line = line.strip()
    root = ET.fromstring(line)
    if (root.attrib['PostTypeId'] == "2") and ('OwnerUserId' in root.attrib):
        print "{0}\t{1}".format(root.attrib['OwnerUserId'], root.attrib['ParentId'])