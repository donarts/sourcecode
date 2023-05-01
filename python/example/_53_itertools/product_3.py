import itertools

A = [1, 2, 3]
B = [4, 5]
C = [6, 7]

sets = itertools.product(A, B, C)
for s in sets:
    print(s)

'''
(1, 4, 6)
(1, 4, 7)
(1, 5, 6)
(1, 5, 7)
(2, 4, 6)
(2, 4, 7)
(2, 5, 6)
(2, 5, 7)
(3, 4, 6)
(3, 4, 7)
(3, 5, 6)
(3, 5, 7)
'''

