#!/usr/bin/env python

import sys

flag = 1

count = ""
page = ""

for line in sys.stdin:
    if flag:
        count, page = line.strip().split('\t')
        print "Most popular page: "+page
        flag = 0