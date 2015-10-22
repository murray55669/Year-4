#!/usr/bin/env python

import sys

for line in sys.stdin:
    line = line.strip()
    
    word_1, word_2, value = line.split("\t", 2)
    
    print("{0}\t{1}\t{2}".format(value, word_1, word_2))