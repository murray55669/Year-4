#!/usr/bin/python

import sys
import re

test = ['userp2.snowhill.com - - [05/Aug/1995:14:57:06 -0400] "GET / " HTTP/1.0" 200 7034',
        'userp2.snowhill.com - - [05/Aug/1995:14:57:06 -0400] "GET .gif HTTP/1.0" 200 7034']


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
        
        page = request[1:-1].split(' ', 1)
        page = page[1].rsplit(' ', 1)
        
        #throw away GET variables
        page = page[0].split('?')
        #throw away .gifs
        if not(page[0][-3:] == "gif"):
            print page[0]
    except:
        break
        #print "Failed on line: "+line
        """
        The lines this fails on:
        
        titan - - [31/Aug/1995:05:06:15 -0400] "?" 400 -  
        128.159.144.83 - - [14/Aug/1995:15:51:37 -0400] "<random characters>" 400 -      
        128.159.144.83 - - [14/Aug/1995:15:52:23 -0400] "<random characters>" 400 -      
        163.206.42.13 - - [31/Aug/1995:11:04:42 -0400] "<random characters> including a newline" 400 -    
        163.206.42.13 - - [31/Aug/1995:11:04:49 -0400] "<random characters> including a newline" 400 -       
        128.159.144.83 - - [14/Aug/1995:15:51:58 -0400] "<random characters>" 400 -      
        128.159.144.83 - - [14/Aug/1995:15:59:35 -0400] "<random characters>" 400 -      
        bloor.torfree.net - - [22/Aug/1995:14:55:16 -0400] "huttle/countdown/" 400 -    

        can probably be safely discarded 
        ('k7us70a.krhm.jvc-victor.co.jp - - [06/Aug/1995' is the only line that fails in the small file)
        """
