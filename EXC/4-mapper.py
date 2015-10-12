#!/usr/bin/python

import sys

for line in sys.stdin:                  # input from standard input
    line = line.strip()                 # remove whitespaces
    tokens = line.split()

    for i in range(0, len(tokens)-1):
        print("{0}\t{1}\t{2}".format(tokens[i], tokens[i+1], 1))