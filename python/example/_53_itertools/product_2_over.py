import itertools

SET = [[1, 2, 3], [4, 5], [6, 7], [8, 9]]


def product_2(A ,B = []):
    if len(B) == 0:
        return A
    if len(A) == 0:
        return B
    sets = itertools.product(A, B)
    r = []
    for s in sets:
        r.append(s)
    return r

def list_extend(list_of_lists):
    result = []
    for item in list_of_lists:
        if type(item)==tuple or type(item)==list:
            result.extend(item)
        else:
            result.append(item)
    return result

def product_multi(set_list):
    result = []
    for i in range(len(set_list)):
        result = product_2(result, set_list[i])
        if i<=1: continue
        result2 = []
        for rone in result:
            result2.append(list_extend(rone))
        result = result2
    return result

print(product_2([],[1, 2]))
# [1, 2]
print(product_2([1,2],[3]))
# [(1, 3), (2, 3)]
print(product_2([(1, 3), (2, 3)],[4]))
# [((1, 3), 4), ((2, 3), 4)]
print(list_extend(((1, 3), 4)))
# [1, 3, 4]
print(product_multi(SET))
# [[1, 4, 6, 8], [1, 4, 6, 9], [1, 4, 7, 8], [1, 4, 7, 9], [1, 5, 6, 8], [1, 5, 6, 9], [1, 5, 7, 8], [1, 5, 7, 9], [2, 4, 6, 8], [2, 4, 6, 9], [2, 4, 7, 8], [2, 4, 7, 9], [2, 5, 6, 8], [2, 5, 6, 9], [2, 5, 7, 8], [2, 5, 7, 9], [3, 4, 6, 8], [3, 4, 6, 9], [3, 4, 7, 8], [3, 4, 7, 9], [3, 5, 6, 8], [3, 5, 6, 9], [3, 5, 7, 8], [3, 5, 7, 9]]

