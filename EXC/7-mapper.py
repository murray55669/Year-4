#!/usr/bin/python

import sys

test = ["0\t7 9 3 6",
        "1\t4 2 9 8",
        "2\t4 6 6 1"]

#for line in sys.stdin:                  # input from standard input
for line in test:
    line = line.strip()                 # remove whitespaces
    tokens = line.split("\t")
    row = tokens[0]
    values = tokens[1].split()
    
    for i in range(0, len(values)):
        print("{0}\t{1}\t{2}".format(i, row, values[i]))