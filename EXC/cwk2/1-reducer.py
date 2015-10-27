#!/usr/bin/python

import sys

current_word = ""
current_document = ""

first_line = 1

document_names = []
word_counts = []
output_tuples = ""

for line in sys.stdin:
    #input = '<word>:<document>' pairs
    #output = '<word>:<total documents word appears in>:{(<document>,<count in document>), ..}'
    line = line.strip()
    word, document = line.split(':')
    
    if first_line:
        current_word = word
        current_document = document
        word_counts.append(0)
        document_names.append(document)
        first_line = 0
        
    if word == current_word and document == current_document:
        word_counts[-1] += 1
    elif word == current_word:
        word_counts.append(1)
        document_names.append(document)
        
        current_document = document
    else:
        for i in range(0, len(document_names)):
            output_tuples += "({0},{1}) ".format(document_names[i],word_counts[i])
        
            
        print("{0}:{1}:{{{2}}}".format(current_word, len(document_names), output_tuples[:-1]))

        
        document_names = []
        word_counts = []
        output_tuples = ""
        
        current_word = word
        current_document = document
        
        word_counts.append(1)
        document_names.append(document)
        
#handle last line
for i in range(0, len(document_names)):
    output_tuples += "({0},{1}) ".format(document_names[i],word_counts[i])
    
print("{0}:{1}:{{{2}}}".format(current_word, len(document_names), output_tuples[:-1]))