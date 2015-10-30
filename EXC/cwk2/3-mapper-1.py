#!/usr/bin/python

import sys

ip = ""
timestamp = ""
request = ""
reply = ""
bytes = ""
rest = []

page = ""

for line in sys.stdin:
    line = line.strip()
    try:
            
        ip, rest = line.split('- -', 1)
        timestamp, rest = rest.split('[', 1)[1].split(']', 1)
        rest, bytes = rest.rsplit(' ', 1)
        rest, reply = rest.rsplit(' ', 1)
        request = rest.split('"', 1)[1].rsplit('"', 1)[0]
        
        
        page = request.split(' ', 1)[1].rsplit(' ', 1)[0]
        #if the page is meaningful
        if not (page.strip() == ""):
            #throw away GET variables
            page = page.split('?')[0]
            #throw away .gifs
            if not(page[-3:] == "gif"):
                print page
    except:
        pass
        #Fails on a bunch of nonsensical records