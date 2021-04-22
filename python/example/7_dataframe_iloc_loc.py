# dataframe example
import pandas as pd
import numpy as np

df = pd.DataFrame(data=np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]), index= [2, 'A', 4, 5], columns=[48, 49, 50])
print(df)

'''
      (48   49   50) <~~~ columns
                   
  2    1    2    3
                   
  A    4    5    6
                   
  4    7    8    9
                   
  5   10   11   12
  ^               
  +------index
'''

#Base
print(df.index)
'''
Index([2, 'A', 4, 5], dtype='object')
'''
print(list(df.index))
'''
[2, 'A', 4, 5]
'''
print(df.columns)
'''
Int64Index([48, 49, 50], dtype='int64')
'''
print(df.shape)
'''
(4, 3)
'''

#select row
print(df.iloc[1])
'''
48    4
49    5
50    6
Name: A, dtype: int32

      (48   49   50) <~~~ columns
                   
  2    1    2    3    <-iloc[0]
    +---------------+
  A |  4    5    6  | <-iloc[1]
    +---------------+
  4    7    8    9    <-iloc[2]
                      
  5   10   11   12    <-iloc[3]
  ^               
  +------index
'''
print(df.loc['A'])
'''
48    4
49    5
50    6
Name: A, dtype: int32

      (48   49   50) <~~~ columns
                   
  2    1    2    3    <-loc[2]
    +---------------+
  A |  4    5    6  | <-loc['A']
    +---------------+
  4    7    8    9    <-loc[4]
                      
  5   10   11   12    <-loc[5]
  ^               
  +------index
'''
print(df.loc[4])
'''
48    7
49    8
50    9
Name: 4, dtype: int32

      (48   49   50) <~~~ columns
                   
  2    1    2    3    <-loc[2]
                      
  A    4    5    6    <-loc['A']
    +---------------+
  4 |  7    8    9  | <-loc[4]
    +---------------+
  5   10   11   12    <-loc[5]
  ^
  +------index
'''

#select column
print(df[48])
'''
2     1
A     4
4     7
5    10
Name: 48, dtype: int32

      (48   49   50) <~~~ columns
     +---+           
  2  | 1 |  2    3   
     |   |           
  A  | 4 |  5    6   
     |   |           
  4  | 7 |  8    9   
     |   |           
  5  |10 | 11   12    
     +---+           
    df[48]df[49]df[50]

'''

#select cell
print(df[48].iloc[2])
'''
7
      (48   49   50) <~~~ columns
     +---+           
  2  | 1 |  2    3   <-iloc[0] loc[2]
     |   |           
  A  | 4 |  5    6   <-iloc[1] loc['A']
     +===+---------+ 
  4  | 7 |  8    9 | <-iloc[2] loc[4]
     +===+---------+ 
  5  |10 | 11   12   <-iloc[3] loc[5]
     +---+            
'''
print(df[48].loc[4])
'''
7
      (48   49   50) <~~~ columns
     +---+           
  2  | 1 |  2    3   <-iloc[0] loc[2]
     |   |           
  A  | 4 |  5    6   <-iloc[1] loc['A']
     +===+---------+ 
  4  | 7 |  8    9 | <-iloc[2] loc[4]
     +===+---------+ 
  5  |10 | 11   12   <-iloc[3] loc[5]
     +---+            
'''
print(df[48][4])
'''
7
      (48   49   50) <~~~ columns
     +---+           
  2  | 1 |  2    3   <-iloc[0] loc[2]   [2]
     |   |           
  A  | 4 |  5    6   <-iloc[1] loc['A'] ['A']
     +===+---------+ 
  4  | 7 |  8    9 | <-iloc[2] loc[4]   [4]
     +===+---------+ 
  5  |10 | 11   12   <-iloc[3] loc[5]
     +---+            
'''