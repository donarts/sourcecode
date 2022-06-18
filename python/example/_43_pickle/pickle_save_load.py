import pickle

data1 = ["xso", 10, 100,{"test":"hello","kim":"illy"}]
data2 = {"ver":1, "tar":2, "zcb":[3,2,1]}
data3 = 20

print(data1)
print(data2)
print(data3)

with open("test.pickle", "wb") as f:
    pickle.dump(data1, f)
    pickle.dump(data2, f)
    pickle.dump(data3, f)


with open("test.pickle", "rb") as f:
    l1 = pickle.load(f)
    l2 = pickle.load(f)
    l3 = pickle.load(f)

print(l1)
print(l2)
print(l3)
'''
['xso', 10, 100, {'test': 'hello', 'kim': 'illy'}]
{'ver': 1, 'tar': 2, 'zcb': [3, 2, 1]}
20
['xso', 10, 100, {'test': 'hello', 'kim': 'illy'}]
{'ver': 1, 'tar': 2, 'zcb': [3, 2, 1]}
20
'''