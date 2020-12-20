#KMeans
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
import random

x = [random.randrange(1,100) for n in range(0,100)]
y = [random.randrange(1,100) for n in range(0,100)]

data = pd.DataFrame({"x":x,"y":y})
print(data)
'''
     x   y
0   32   1
1   49  99
2   78  21
..  ..  ..
[100 rows x 2 columns]
'''
# 모델 만들기
model = KMeans(n_clusters=3)
# 학습
model.fit(data)
# predict
predictions = model.predict(data)

# 그림을 그리기 쉽게하기 학위해서 예측 결과를 dataframe으로 만들어서 붙이기
predict = pd.DataFrame(predictions)
predict.columns=['predict']
# concatenate labels to df as a new column
r = pd.concat([data,predict],axis=1)
print(r)
'''
     x   y  predict
0   32   1        0
1   49  99        1
2   78  21        2
..  ..  ..      ...
[100 rows x 3 columns]
'''
# 그림 그리기
plt.scatter(r['x'],r['y'],c=r['predict'])
plt.show()

# 임의의 하나의 데이터 입력하여 예측, input one data
prediction = model.predict([[1,100]])
print(prediction)
'''
[1]
'''

'''
Result

     x   y
0    5  50
1   39  38
2   20  98
3   93   2
4   16   6
..  ..  ..
95  62  41
96  76  73
97  61  11
98  97  27
99  48  36

[100 rows x 2 columns]
     x   y  predict
0    5  50        2
1   39  38        2
2   20  98        1
3   93   2        0
4   16   6        2
..  ..  ..      ...
95  62  41        0
96  76  73        1
97  61  11        0
98  97  27        0
99  48  36        0

[100 rows x 3 columns]
[1]
'''

