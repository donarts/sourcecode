import numpy as np

####################################### 데이터 준비
data_count = 5000
np.random.seed(42)
# np.random.rand(m,n) n*m matrix 로 0~1 랜덤 생성
x = np.random.rand(data_count, 3)
'''
[[0.37454012 0.95071431 0.73199394]
 [0.59865848 0.15601864 0.15599452]
 [0.05808361 0.86617615 0.60111501]
 ...
'''
x_one_d = x[:,0:1] * x[:,1:2] * x[:,2:3]
'''
[[2.60648878e-01]  # <= [0.37454012 * 0.95071431 * 0.73199394]
 [1.45701819e-02]
 [3.02424805e-02]
 ...
'''

# y는 원하는 값 목표값인 label로 표현합니다.
y = 1 + 2 * x_one_d + .1 * np.random.randn(data_count, 1)
'''
[[1.52585494]
 [0.96398033]
 [1.27487937]
 ...
'''
# 저장전 확인
print(x.shape,type(x),x[0])
print(y.shape,type(y),y[0])

# 저장
np.savetxt("x_data.csv", x, delimiter=',')
np.savetxt("y_data.csv", y, delimiter=',')

# 저장된것 확인
x_data = np.loadtxt("x_data.csv", delimiter=',', skiprows=0, max_rows=1)
print(x_data.shape,type(x_data),x_data)
if x_data.shape==():
    x_data = np.array([x_data]) 
print(x_data.shape,type(x_data),x_data)
y_data = np.loadtxt("y_data.csv", delimiter=',', skiprows=0, max_rows=1)
print(y_data.shape,type(y_data),y_data)
if y_data.shape==():
    y_data = np.array([y_data]) 
print(y_data.shape,type(y_data),y_data)