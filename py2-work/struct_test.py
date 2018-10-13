import sys
import struct
import csv

sb = struct.pack(">h", 2006)
print len(sb)

s = struct.unpack(">h", sb)
print s

print struct.unpack(">2c", sb)

fb = struct.pack(">f", 2006.0001)
print len(fb)

f = struct.unpack(">f", fb)
print f

print struct.unpack(">4c", fb)

file = open("ttt.dat", "wb")
file.write(sb)
file.write(fb)
file.close()