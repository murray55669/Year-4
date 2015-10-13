#!/usr/bin/python

import sys

#mark -> couseID, studentID, grade
#student -> studentID, name

for line in sys.stdin:
    line = line.strip()
    tokens = line.split()
    tag = tokens[0]

    if tag == "student":
        #print (studentID, name)
        print("{0}\t{1}".format(tokens[1], tokens[2]))
    else:
        #print(studentID, courseID, grade)
        print("{0}\t{1}\t{2}".format(tokens[2], tokens[1], tokens[3]))