#!/usr/bin/python

import sys

prev_line = ""
line = ""
first_line = 1;

for line in sys.stdin:
    line = line.strip()

    if first_line:
        print line
        prev_line = line
        first_line = 0
    else:
        if line == prev_line:
            pass
        else:
            print line
            prev_line = line