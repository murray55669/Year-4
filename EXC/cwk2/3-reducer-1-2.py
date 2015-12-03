#!/usr/bin/env python

import sys

count = ""
count_max = 0
page = ""
page_max = ""

for line in sys.stdin:
    count, page = line.strip().split('\t')
    if int(count) > count_max:
        count_max = int(count)
        page_max = page
        
print "Most popular page: "+page_max