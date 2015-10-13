#!/usr/bin/python

import sys

for line in sys.stdin:
    line = line.strip()
    tokens = line.split()

    for i in range(0, len(tokens)-1):
        print("{0}\t{1}\t{2}".format(tokens[i], tokens[i+1], 1))