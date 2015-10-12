#!/usr/bin/python

import sys

for line in sys.stdin:                  # input from standard input
    line = line.strip()                 # remove whitespaces

    word_1, word_2, value = line.split("\t", 2)
    
    print("{0}\t{1}\t{2}".format(value.zfill(9), word_1, word_2))