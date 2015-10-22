#!/usr/bin/env python

import sys

lowest = 1

for line in sys.stdin:
    line = line.strip()
    mark, name = line.split()
    
    if lowest:
        print(name+" with "+mark)
        lowest = 0