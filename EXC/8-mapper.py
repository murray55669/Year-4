#!/usr/bin/python

import sys

test = ["student\t0\tGeorge",
        "mark\tEXC\t0\t70",
        "student\t1\tAnna",
        "mark\tADBS\t0\t80",
        "mark\tEXC\t1\t65",
        "mark\tTTS\t0\t80"]

#mark -> couseID, studentID, grade
#student -> studentID, name

#for line in sys.stdin:                  # input from standard input
for line in test:
    line = line.strip()                 # remove whitespaces
    tokens = line.split("\t")
    tag = tokens[0]
    
    if tag == "student":
        #print (studentID, name)
        print("{0}\t{1}".format(tokens[1], tokens[2]))
    else:
        #print(studentID, courseID, grade
        print("{0}\t{1}\t{2}".format(tokens[2], tokens[1], tokens[3]))