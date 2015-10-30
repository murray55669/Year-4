#!/usr/bin/python

import sys

first_line = 1

count = ""
user = ""
posts_answered = ""

for line in sys.stdin:
    if first_line:
        count, user, posts_answered = line.strip().split("\t")
        print "{0}\t-> {1}".format(user, posts_answered[:-1])
        first_line = 0