#!/usr/bin/python

import sys

ip = ""
timestamp = ""
request = ""
reply = ""
bytes = ""
rest = []

for line in sys.stdin:
    line = line.strip()
    try:
            
        ip, rest = line.split('- -', 1)
        timestamp, rest = rest.split('[', 1)[1].split(']', 1)
        rest, bytes = rest.rsplit(' ', 1)
        rest, reply = rest.rsplit(' ', 1)
        request = rest.split('"', 1)[1].rsplit('"', 1)[0]
        
        if reply == "404":
            print ip
        
    except:
        pass