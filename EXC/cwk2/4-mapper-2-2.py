#!/usr/bin/python

import sys

count = ""
count_max = 0
user = ""
user_max = ""
posts_answered = ""
posts_answered_max = ""

for line in sys.stdin:
    count, user, posts_answered = line.strip().split("\t")
    if int(count) > count_max:
        count_max = int(count)
        user_max = user
        posts_answered_max = posts_answered
        
print "{0}\t{1}\t{2}".format(count_max, user_max, posts_answered_max)