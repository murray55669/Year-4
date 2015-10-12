#!/usr/bin/python

import sys
import random

for line in sys.stdin:
    for w in line.split():
        print '%s\t%d' % (w, random.randint(1, 100))
