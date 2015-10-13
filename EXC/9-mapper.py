#!/usr/bin/python

import sys

#Name --> (courseID,grade) (courseID,grade) ...

for line in sys.stdin:
    line = line.strip()
    tokens = line.split()
    name = tokens[0]
    marks = tokens[2:]
    subjects = len(marks)
    total = 0.0

    if subjects >= 4:
        for tuple in marks:
            mark = int(tuple.split(",")[1][:-1])
            total += mark
        print(str(total/subjects)+" "+name)