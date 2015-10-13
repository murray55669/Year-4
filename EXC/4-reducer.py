#!/usr/bin/python

import sys

prev_word_1 = ""
prev_word_2 = ""
value_total = 0
word_1 = ""
word_2 = ""

for line in sys.stdin:
    line = line.strip()
    word_1, word_2, value = line.split("\t", 2)
    value = int(value)
    if prev_word_1 == word_1 and prev_word_2 == word_2:
        value_total += value
    else:
        if prev_word_1 and prev_word_2:
            print("{0}\t{1}\t{2}".format(prev_word_1, prev_word_2, value_total))
            
        value_total = value
        prev_word_1 = word_1
        prev_word_2 = word_2

if prev_word_1 == word_1 and prev_word_2 == word_2:
    print("{0}\t{1}\t{2}".format(prev_word_1, prev_word_2, value_total))