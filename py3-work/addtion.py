# coding=utf-8

from itertools import permutations

list_a = list(permutations("234567890"))
for item in list_a:
    a = int(''.join(item[0:3]))
    b = int(''.join(item[3:6]))
    c = int(''.join(item[6:9])) + 1000
    if a + b == c:
        print("  %d\n+ %d\n-----\n %d\n" % (a, b, c))
