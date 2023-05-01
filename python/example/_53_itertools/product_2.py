import itertools

A = [1, 2, 3]
B = [4, 5]

sets = itertools.product(A, B)
for s in sets:
    print(s)

'''
(1, 4)
(1, 5)
(2, 4)
(2, 5)
(3, 4)
(3, 5)
'''

