#!/usr/bin/python

import sys

prev_word = ""
value_total = 0
word = ""

for line in sys.stdin:          # For ever line in the input from stdin
    line = line.strip()         # Remove trailing characters
    word, value = line.split("\t", 1)
    value = int(value)
    # Remember that Hadoop sorts map output by key reducer takes these keys sorted
    if prev_word == word:
        value_total += value
    else:
        if prev_word:  # write result to stdout
            print("{0}\t{1}".format(prev_word, value_total))
            
        value_total = value
        prev_word = word

if prev_word == word:  # Don't forget the last key/value pair
    print("{0}\t{1}".format(prev_word, value_total))
