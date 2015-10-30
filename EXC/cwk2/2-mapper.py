#!/usr/bin/python

import sys
import os
import math

corpus_size = int(os.getenv('corpus_size'))

score = 0.0

term_list = []
terms = open("terms.txt")
for line in terms:
    term_list.append(line.strip().lower())
terms.close()

term_set = frozenset(term_list)

word = ""
total_docs_containing = ""
tuple_strings = ""
score = 0.0

for line in sys.stdin:
    #input = '<word>:<total documents word appears in>:{(<document>,<count in document>), ..}'
    word, total_docs_containing, tuple_strings = line.strip().split(':')
    if word in term_set:
        tuple_strings = tuple_strings[1:-1].split(' ')
        
        for string in tuple_strings:
            #tuple_split[0] = doc name
            #tuple_split[1] = count
            #tuple_split[2] may exist, is discarded
            tuple_split = string.split(',')
            
            score = float(tuple_split[1][:-1]) * math.log((corpus_size / float(1 + int(total_docs_containing))), 10)
            
            print tuple_split[0][1:] + "," + word + "," + str(score)