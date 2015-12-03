#!/usr/bin/env python

import sys
import bisect

count= ""
host = ""
count_int = 0

top_10 = []

for line in sys.stdin:
    line = line.strip()
    
    count, host = line.split("\t")
    count_int = int(count)
    
    bisect.insort(top_10, (count_int, host))
    if len(top_10) > 10:
        top_10 = top_10[-10:]


for c, h in top_10:
    print("{0}\t{1}".format(c, h))