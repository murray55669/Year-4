#!/usr/bin/python

import sys
import time

epoch = 0

ip = ""
timestamp = ""
request = ""
reply = ""
bytes = ""
rest = []

pattern = '%d/%b/%Y:%H:%M:%S'

for line in sys.stdin:
    line = line.strip()
    try:
        
        ip, rest = line.split('- -', 1)
        timestamp, rest = rest.split('[', 1)[1].split(']', 1)
        rest, bytes = rest.rsplit(' ', 1)
        rest, reply = rest.rsplit(' ', 1)
        request = rest.split('"', 1)[1].rsplit('"', 1)[0]
        
        
        #-14400 seconds is GMT-0400 ; timestamp[:-6] drops the ' -0400'
        epoch = int(time.mktime(time.strptime(timestamp[:-6], pattern)))-14400
        print "{0}\t{1}".format(ip, epoch)
    
       
    except:
        pass