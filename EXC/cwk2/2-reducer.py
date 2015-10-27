#!/usr/bin/python

import sys

for line in sys.stdin:
    #input = 'document,word,score'
    print line.strip()
    #document, word, score = line.split(',')
   # print "{0}, {1} = {2}".format(word, document, score)