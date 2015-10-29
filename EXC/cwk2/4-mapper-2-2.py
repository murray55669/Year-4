#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET


for line in sys.stdin:
    line = line.strip()
    root = ET.fromstring(line)
    if int(root.attrib['PostTypeId']) == 2:
        print "{0}\t{1}".format(root.attrib['OwnerUserId'], root.attrib['ParentId'])