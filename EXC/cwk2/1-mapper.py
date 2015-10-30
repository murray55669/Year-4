#!/usr/bin/python

import sys
import os
import re

file_name_full = os.getenv('map_input_file')
file_name = file_name_full.split("/")[-1]

rx = re.compile('\W+')

for line in sys.stdin:
    #tokenize text
    line = re.sub('_', '', line)
    line = rx.sub(' ', line).strip().lower()

    #Need to output: 'word:filename'
    #Need to ensure all words that are the same go to same reducer
    for word in line.split():
        print("{0}:{1}".format(word, file_name))