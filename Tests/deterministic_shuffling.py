import random

local_seed = 55

a = ['a', 'b', 'c']
b = [1, 2, 3]
c = [10, 20, 30]

aa = a
bb = b
cc = c

lists = list(zip(a, b, c))
random.Random(local_seed).shuffle(lists)

a, b, c = zip(*lists)
print a
print b
print c

del lists
lists = list(zip(aa, bb, cc))
random.Random(local_seed).shuffle(lists)

a, b, c = zip(*lists)
print a
print b
print c
