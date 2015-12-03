#!/usr/bin/python

import sys
import xml.etree.ElementTree as ET
import bisect

root = None

top_10 = []

for line in sys.stdin:
    line = line.strip()
    root = ET.fromstring(line)
    if int(root.attrib['PostTypeId']) == 1:
        bisect.insort(top_10, (int(root.attrib['ViewCount']), root.attrib['Id']))
        if len(top_10) > 10:
            top_10 = top_10[-10:]
            
for vc, id in top_10:
    print "{0}\t{1}".format(vc, id)