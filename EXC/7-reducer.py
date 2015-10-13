#!/usr/bin/python

import sys

current_row = 0
row = []

def print_row(row_index, array):
    line = str(row_index)+"\t"
    for element in array:
        line = line+element+" "
    print(line)

for line in sys.stdin:   
    line = line.strip()
    
    row_index, col_index, val = line.split("\t")
    row_index = int(row_index)
    
    if row_index == current_row:
        row.append(val)
    else:
        print_row(row_index-1, row)
        row = []
        current_row = row_index
        row.append(val)
        
#handle final row
if row_index == current_row:
    print_row(row_index, row)