#!/usr/bin/python

import sys

first_line = 1

count = ""
user = ""
answers = ""

for line in sys.stdin:
    if first_line:
        count, user, answers = line.strip().split("\t")
        print "{0}\t-> {1},\t{2}".format(user, count, answers[:-1])
        first_line = 0