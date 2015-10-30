#!/usr/bin/python

import sys
from time import strftime, gmtime

cur = ""
first_line = 1

first = 0
last = 0

ip = ""
epoch = ""

pattern = '%d/%b/%Y:%H:%M:%S +0000'

for line in sys.stdin:
    line = line.strip()
    
    ip, epoch = line.split("\t")
    
    if first_line:
        first_line = 0
        cur = ip
        
    if not (cur == ip):
        if (first == last):
            print "{0}\t{1}".format(ip, strftime(pattern, gmtime(first)))
        else:
            print "{0}\t{1} seconds".format(ip, (last-first))
        
        cur = ip
        first = int(epoch)
        last = int(epoch)
        
    else:
        last = int(epoch)

#handle last line
if (first == last):
    print "{0}\t{1}".format(ip, strftime(pattern, gmtime(first)))
else:
    print "{0}\t{1} seconds".format(ip, (last-first))