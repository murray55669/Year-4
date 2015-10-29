#!/usr/bin/python

import sys
import re

test = ['userp2.snowhill.com - - [05/Aug/1995:14:57:06 -0400] "GET / " HTTP/1.0" 404 7034',
        'some.ip - - [05/Aug/1995:14:57:06 -0400] "GET .gif HTTP/1.0" 200 7034',
        'some.ip - - [05/Aug/1995:14:57:06 -0400] "GET / " HTTP/1.0" 404 7034',
        'userp2.snowhill.com - - [05/Aug/1995:14:57:06 -0400] "GET / " HTTP/1.0" 404 7034']


#for line in test:
for line in sys.stdin:
    line = line.strip()
    try:
            
        ip, rest = line.split('- -', 1)
        
        timestamp = re.findall('\[.*\]', rest)[0]
        request = re.findall('".*"', rest)[0] 
        rest = re.split('".*"', rest)[1].split(' ')
        reply = rest[1]
        bytes = rest[2]
        
        #print ip
        #print timestamp
        #print request[1:-1]
        #print reply
        #print bytes
        
        if reply == "404":
            print ip
        
    except:
        break
        
