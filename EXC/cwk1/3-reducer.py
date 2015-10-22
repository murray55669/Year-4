#!/usr/bin/python

import sys

word_count = 0
line_count = 0

for line in sys.stdin:
    line = line.strip()

    no_spaces = line.split()
    for word in no_spaces:
        word_count += 1
    
    line_count += 1
    
print str(line_count)+" "+str(word_count)