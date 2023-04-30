import itertools


val = [1, 2, 3]

print("Permutations")
for i in range(1, len(val)+1):
    perm_set = itertools.permutations(val, i)
    for sets in perm_set:
        print(sets)


print("Combinations")
for i in range(1, len(val)+1):
    comb_set = itertools.combinations(val, i)
    for sets in comb_set:
        print(sets)


print("Combinations_with_replacement")
for i in range(1, len(val)+1):
    perm_set = itertools.combinations_with_replacement(val, i)
    for sets in perm_set:
        print(sets)

'''
Permutations
(1,)
(2,)
(3,)
(1, 2)
(1, 3)
(2, 1)
(2, 3)
(3, 1)
(3, 2)
(1, 2, 3)
(1, 3, 2)
(2, 1, 3)
(2, 3, 1)
(3, 1, 2)
(3, 2, 1)
Combinations
(1,)
(2,)
(3,)
(1, 2)
(1, 3)
(2, 3)
(1, 2, 3)
Combinations_with_replacement
(1,)
(2,)
(3,)
(1, 1)
(1, 2)
(1, 3)
(2, 2)
(2, 3)
(3, 3)
(1, 1, 1)
(1, 1, 2)
(1, 1, 3)
(1, 2, 2)
(1, 2, 3)
(1, 3, 3)
(2, 2, 2)
(2, 2, 3)
(2, 3, 3)
(3, 3, 3)
'''