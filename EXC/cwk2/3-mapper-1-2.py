#!/usr/bin/env python

import sys

count = ""
count_max = 0
page = ""
page_max = ""

for line in sys.stdin:
    line = line.strip()
        
    count, page = line.split("\t")
    if int(count) > count_max:
        count_max = int(count)
        page_max = page
    

print "{0}\t{1}".format(count_max, page_max)