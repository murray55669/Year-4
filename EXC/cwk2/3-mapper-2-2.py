#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    
    count, host = line.split("\t")
    
    print("{0}\t{1}".format(count, host))