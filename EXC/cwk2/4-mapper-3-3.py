#!/usr/bin/python

import sys

count = ""
user = ""
answers = ""
count_max = 0
user_max = ""
answers_max = ""

for line in sys.stdin:
    count, user, answers = line.strip().split("\t")
    
    if int(count) > count_max:
        count_max = int(count)
        user_max = user
        answers_max = answers
        
print "{0}\t{1}\t{2}".format(count_max, user_max, answers_max)