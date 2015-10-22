#!/usr/bin/python

import sys

current_student = 0
name = ""
grades = []

def print_data(name, grades):
    line = name+" --> "
    for grade in grades:
        line = line+"("+grade[0]+","+grade[1]+") "
    print line

for line in sys.stdin:
    line = line.strip()
    
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