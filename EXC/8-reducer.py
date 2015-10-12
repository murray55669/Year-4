#!/usr/bin/python

import sys

test = [
"0\tADBS\t80",
"0\tEXC\t70",
"0\tGeorge",
"0\tTTS\t80",
"1\tAnna",
"1\tEXC\t65"]

current_student = 0
prev_line = ""
name = ""
grades = []

def print_data(name, grades):
    line = name+" --> "
    for grade in grades:
        line = line+"("+grade[0]+","+grade[1]+") "
    print line

for line in sys.stdin:          # For ever line in the input from stdin
#for line in test:
    if line != prev_line:
        prev_line = line
        line = line.strip()         # Remove trailing characters
        
        tokens = line.split("\t")
        student_id = int(tokens[0])
        
        if current_student != student_id:
            print_data(name, grades)
            grades = []
            current_student = student_id
                
        #student record
        if len(tokens) == 2:
            name = tokens[1]
        #course record
        else:
            grades.append((tokens[1], tokens[2]))
                

print_data(name, grades)