#!/usr/bin/python

import sys

counts = {}

for line in sys.stdin:
    line = line.strip()
    tokens = line.split()

    for i in range(0, len(tokens)-1):
        tuple = (tokens[i], tokens[i+1])
        if not counts:
            counts[tuple] = 1
        else:
            if tuple in counts:
                counts[tuple] += 1
            else:
                counts[tuple] = 1
                
    for (key_1, key_2) in counts:
        value = counts.get((key_1, key_2))
        print("{0}\t{1}\t{2}".format(key_1, key_2, value))
    counts.clear()