#!/usr/bin/env python

import sys

total = 0

for line in sys.stdin:
    if total < 10:
        count, host = line.strip().split('\t')
        print "Count: "+count+" Host: "+host
        total += 1