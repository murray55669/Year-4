#!/usr/bin/python

import sys
import os

file_name_full = os.getenv('map_input_file')
file_name = file_name_full.split("/")[-1]

for line in sys.stdin:
    #Need to output: 'word:filename'
    #Need to ensure all words that are the same go to same reducer
    for word in line.strip().split(' '):
        print("{0}:{1}".format(word, file_name))