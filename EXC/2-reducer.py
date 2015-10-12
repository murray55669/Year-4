#!/usr/bin/python

import sys

prev_line = ""
line = ""
first_line = 1;

for line in sys.stdin:          # For ever line in the input from stdin
    line = line.strip()         # Remove trailing characters

    if first_line:              # If first line, print no matter what
        print line
        prev_line = line
        first_line = 0
    else:                       # If not the first line, check if we've seen this line before
        if line == prev_line:
            pass
        else:
            print line
            prev_line = line