#!/usr/bin/python

import sys

cur = ""
first = 1
count = 0

for line in sys.stdin:
    line = line.strip()
    
    if first:
        first = 0
        cur = line
        
    if not (cur == line):
        print "{0}\t{1}".format(count, cur)
        cur = line
        count = 1
    else:
        count += 1

#handle last line
print "{0}\t{1}".format(count, cur)