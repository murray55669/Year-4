import hashlib

m = hashlib.md5()

str = "\x00\xf9\x19\x94\x4a\xf3\x10\x92\x32\x98\x11\x8c\x33\x27\x91\xeb"

"""
String: \x55\x4e\x62\x4e\x6c\x52\x55\x44\x45\x62\x43\x50\x63\x56\x67\x73\x00
Digest: \x96\x03\xd1\xa8\xcb\xdf\x4f\xaf\x13\xec\x60\xf5\x67\x00\x91\xeb
"""

m.update(str)
digest = m.digest()

print "String: " + ''.join(x.encode('hex') for x in str)
print "Digest: x"+'\\x'.join(x.encode('hex') for x in digest)
print ''.join(x.encode('hex') for x in digest)