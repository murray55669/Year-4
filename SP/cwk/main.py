import hashlib
from random import choice
from string import ascii_letters

m = None

str = ''
count = 0

digest = ''

END = '\x00\x91\xeb'

while True:
    count += 1
    1
    str = ''.join(choice(ascii_letters) for i in range(16)) + "\x00"
    m = hashlib.md5()
    m.update(str)
    
    digest = m.digest()
    
    if digest[-3:] == END and "\20" not in digest and "\20" not in str and "\99" not in digest and "\99" not in str:
        print "String: \\x"+'\\x'.join(x.encode('hex') for x in str)
        print "Digest: \\x"+'\\x'.join(x.encode('hex') for x in digest)
        print "Attempts:", count
        break