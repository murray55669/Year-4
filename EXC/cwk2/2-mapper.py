#!/usr/bin/python

import sys
import os
import math
import logging

#corpus_size = os.getenv('corpus_size')
corpus_size = 4

test = ["bear:1:{(d2.txt,1)}",
        "cat:2:{(d1.txt,2), (d2.txt,3)}",
        "dog:2:{(d1.txt,1), (d3.txt,1)}",
        "000:2:{(d1.txt,10) (d5.txt,1)}"]

score = 0.0

term_list = []
terms = open("terms.txt")
for line in terms:
    term_list.append(line.strip())
terms.close()

term_set = frozenset(term_list)

logging.warn(term_set)

#for line in sys.stdin:
for line in test:
    #input = '<word>:<total documents word appears in>:{(<document>,<count in document>), ..}'
    word, total_docs_containing, tuple_strings = line.strip().split(':')
    if not word in term_set:
        tuple_strings = tuple_strings[1:-1].split(' ')
        
        for string in tuple_strings:
            #tuple_split[0] = doc name
            #tuple_split[1] = count
            #tuple_split[2] may exist, is discarded
            tuple_split = string.split(',')
            
            score = float(tuple_split[1][:-1]) * math.log((corpus_size / float(1 + int(total_docs_containing))), 10)
            

            #print "{0},{1},{2}".format(tuple_split[0][1:], word, score)
            print tuple_split[0][1:] + "," + word + "," + str(score)


    
    