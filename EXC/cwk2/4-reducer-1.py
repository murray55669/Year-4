#!/usr/bin/python

import sys

total = 0

for line in sys.stdin:
    if total < 10:
        views, id = line.strip().split('\t')
        
        print "{0},\t{1}".format(id, views)
    
        total += 1
    