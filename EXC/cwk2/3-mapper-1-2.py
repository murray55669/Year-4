#!/usr/bin/env python

import sys

count = ""
page = ""

for line in sys.stdin:
    line = line.strip()
        
    count, page = line.split("\t")
    
    print "{0}\t{1}".format(count, page)