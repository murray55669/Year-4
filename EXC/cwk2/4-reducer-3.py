#!/usr/bin/python

import sys

first_line = 1

accepted = ""
owner = ""

count = 0

accepted_id = ""
owner_id = ""

for line in sys.stdin:
    #input: either 'acceptedID, 0' or 'acceptedID, ownerID'
    #emit 'ownerID, acceptedID' pairs
    accepted_id, owner_id = line.strip().split("\t")
    
    if first_line:
        first_line = 0
        accepted = accepted_id
        
    if accepted == accepted_id:
        count += 1
        
        if not (owner_id == "0"):
            owner = owner_id            
        
    else:
        #if we have seen a pair, emit the pair
        if count == 2:
            print "{0}\t{1}".format(owner, accepted)
            
        count = 1
        accepted = accepted_id
        if not (owner_id == "0"):
            owner = owner_id
            
#handle last line
if count == 2:
    print "{0}\t{1}".format(owner, accepted)