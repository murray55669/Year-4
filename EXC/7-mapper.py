#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.strip()
    tokens = line.split("\t")
    row = tokens[0]
    values = tokens[1].split()
    
    for i in range(0, len(values)):
        print("{0}\t{1}\t{2}".format(i, row, values[i]))