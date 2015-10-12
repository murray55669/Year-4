#!/usr/bin/python

import sys

test =  ["0\t0\t7",
        "0\t1\t4",
        "0\t2\t4",
        "1\t0\t9",
        "1\t1\t2",
        "1\t2\t6",
        "2\t0\t3",
        "2\t1\t9",
        "2\t2\t6",
        "3\t0\t6",
        "3\t1\t8",
        "3\t2\t1"]


current_row = 0
row = []

def print_row(row_index, array):
    line = str(row_index)+"\t"
    for element in array:
        line = line+element+" "
    print(line)

#for line in sys.stdin:          # For ever line in the input from stdin
for line in test:
    line = line.strip()         # Remove trailing characters
    
    row_index, col_index, val = line.split("\t")
    row_index = int(row_index)
    
    if row_index == current_row:
        row.append(val)
    else:
        print_row(row_index, row)
        row = []
        current_row = row_index
        row.append(val)
        
#handle final row
if row_index == current_row:
    print_row(row_index, row)
    
