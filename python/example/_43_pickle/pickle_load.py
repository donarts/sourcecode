import pickle

with open("test.pickle", "rb") as f:
    l1 = pickle.load(f)
    l2 = pickle.load(f)
    l3 = pickle.load(f)

print(l1)
print(l2)
print(l3)

'''
binary 조작할때 다양한 종류의 오류가 발생함
수정을 해도 문제 발생 하지 않는 경우도 있음

C:\Users\example\_43_pickle>python pickle_load.py
['xso', 10, 100, {'test': 'hello', 'kim': 'illy'}]
{'ver': 1, 'tar': 2, 'zcb': [3, 2, 1]}
20

C:\Users\example\_43_pickle>python pickle_load.py
Traceback (most recent call last):
  File "pickle_load.py", line 5, in <module>
    l2 = pickle.load(f)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x94 in position 3: invalid start byte

C:\Users\example\_43_pickle>python pickle_load.py
Traceback (most recent call last):
  File "pickle_load.py", line 5, in <module>
    l2 = pickle.load(f)
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x94 in position 3: invalid start byte

C:\Users\example\_43_pickle>python pickle_load.py
Traceback (most recent call last):
  File "pickle_load.py", line 5, in <module>
    l2 = pickle.load(f)
MemoryError
'''