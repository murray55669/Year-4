#!/usr/bin/python

import sys

current_user = ""
current_post = ""
count = 0
answered = ""

first_line = 1

user = ""
post = ""

for line in sys.stdin:
    user, post = line.strip().split("\t")
    
    if first_line:
        first_line = 0
        
        current_user = user
        current_post = post
        
        answered += post+", "
        count += 1
        
    if current_user == user:
        if not (post == current_post):
            #prevent cases where a user answered the same post twice
            answered += post+", "
            count += 1
        
    else:
        print "{0}\t{1}\t{2}".format(count, current_user, answered)
        current_user = user
        current_post = post
        count = 1
        answered = post+", "
    
#handle last line
print "{0}\t{1}\t{2}".format(count, current_user, answered)