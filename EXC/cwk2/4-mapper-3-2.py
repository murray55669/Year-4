#!/usr/bin/python

import sys

for line in sys.stdin:
    #input: 'ownerID, acceptedID' pairs
    line = line.strip()
    print line