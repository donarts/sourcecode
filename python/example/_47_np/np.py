import numpy as np
a = np.array([[ 0,  1,  2,  3,  4],[ 5,  6,  7,  8,  9],[10, 11, 12, 13, 14]])
print(f"array {a}")
print(f"np.ndim {a.ndim}")
print(f"np.shape {a.shape}")
print(f"np.size {a.size}")
print(f"np.dtype {a.dtype}")
print(f"np.itemsize {a.itemsize}")
print(f"np.data {a.data}")
'''
array [[ 0  1  2  3  4]
 [ 5  6  7  8  9]
 [10 11 12 13 14]]
np.ndim 2
np.shape (3, 5)
np.size 15
np.dtype int32
np.itemsize 4
np.data <memory at 0x0000011CC5EBAEE0>
'''

c = np.arange(24)
print(f"array {c}")
print(f"array {c.reshape(2,3,4)}")
print(f"array {c.reshape(-1,3,4)}")
'''
array [ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23]
array [[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]

 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
array [[[ 0  1  2  3]
  [ 4  5  6  7]
  [ 8  9 10 11]]

 [[12 13 14 15]
  [16 17 18 19]
  [20 21 22 23]]]
'''