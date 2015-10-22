#!/usr/bin/python

import sys
import os
import re

#file_name = "filename"
file_name_full = os.getenv('map_input_file')
file_name = file_name_full.split("/")[-1]

test = ["""Libraries destroyed by Fire.--Alexandrian.--St. Paul's destruction
  of MSS., Value of.--Christian books destroyed by Heathens.--Heathen
  books destroyed by Christians.--Hebrew books burnt at Cremona.""",
  """17. ISRAEL'S GREAT RESOLVE
     18. THE LIGHT-BORN MESSENGER
     19. THE RAINBOW SIGN
     20. LIFE'S NEW LANGUAGE
     21. ISRAEL IN PRISON
     22. HOW NAOMI TURNED MUSLIMA
     23. ISRAEL'S RETURN FROM PRISON
     24. THE ENTRY OF THE SULTAN
""",
"""_Within sight of an English port, and within hail of English ships as
they pass on to our empire in the East, there is a land where the ways
of life are the same to-day as they were a thousand years ago; """,
"""'I wondered what old Mr. Abraham Hayward...
  and
  'I knew that if I leaned forward...




ENOCH SOAMES
"""]

for line in sys.stdin:
#for line in test:
    line = re.sub('[-\']', '', line)
    line = re.sub('_', '', line)
    rx = re.compile('\W+')
    line = rx.sub(' ', line).strip().lower()

    #Need to output: filename, word, count of word(?)
    #Needs to be sorted by word
    for word in line.split():
        print("{0}:{1}".format(word, file_name))