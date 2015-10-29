#!/usr/bin/python

import sys

for line in sys.stdin:
    #input = 'document,word,score'
    document, word, score = line.strip().split(',')
    print "{0}, {1} = {2}".format(word, document, score)
   
