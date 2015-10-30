#!/usr/bin/python

import sys

first_line = 1

owner = ""
accepted = ""

count = 0

ownerID = ""
acceptedID = ""

for line in sys.stdin:
    #input: 'ownerID, acceptedID' pairs
    #emit 'count, ownerID, acceptedIDsList'
    ownerID, acceptedID = line.strip().split("\t")
    
    if first_line:
        first_line = 0
        
        owner = ownerID
        
    if ownerID == owner:
        count += 1
        accepted += acceptedID+", "
    
    else:
        print "{0}\t{1}\t{2}".format(count, owner, accepted)
        
        accepted = acceptedID+", "
        count = 1
        owner = ownerID
        
#handle last line
print "{0}\t{1}\t{2}".format(count, owner, accepted)