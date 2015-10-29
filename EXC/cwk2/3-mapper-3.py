#!/usr/bin/python

import sys
import re
import time

test = ['userp2.snowhill.com - - [05/Aug/1995:14:57:06 -0400] "GET / " HTTP/1.0" 200 7034',
        'userp2.snowhill.com - - [05/Aug/1995:16:57:06 -0400] "GET .gif HTTP/1.0" 200 7034']


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
        
        timestamp = timestamp[1:-7]
        pattern = '%d/%b/%Y:%H:%M:%S'
        #-14400 seconds is GMT-0400
        epoch = int(time.mktime(time.strptime(timestamp, pattern)))-14400
        print "{0}\t{1}".format(ip, epoch)
    
       
    except:
        break