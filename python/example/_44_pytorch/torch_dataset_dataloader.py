import torch
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data.dataset import random_split

####################################### 데이터 준비
np.random.seed(42)
# np.random.rand(m,n) n*m matrix 로 0~1 랜덤 생성
x = np.random.rand(100, 3)
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
y = 1 + 2 * x_one_d + .1 * np.random.randn(100, 1)
'''
[[1.52585494]
 [0.96398033]
 [1.27487937]
 ...
'''
################################################

x_tensor = torch.from_numpy(x).float()
y_tensor = torch.from_numpy(y).float()
'''
x_tensor :
tensor([[0.3745, 0.9507, 0.7320],
        [0.5987, 0.1560, 0.1560],
        [0.0581, 0.8662, 0.6011],
        ...
y_tensor:
tensor([[1.5259],
        [0.9640],
        [1.2749],
        ...
'''

class CustomDataset(Dataset):
    def __init__(self, x_tensor, y_tensor):
        self.x = x_tensor
        self.y = y_tensor
        
    def __getitem__(self, index):
        """
        주어진 인덱스 index 에 해당하는 샘플을 데이터셋에서 불러오고 반환합니다.
        """
        return (self.x[index], self.y[index])

    def __len__(self):
        """
        데이터셋의 샘플 개수를 반환합니다.
        """
        return len(self.x)
        
dataset = CustomDataset(x_tensor, y_tensor)

train_dataset, val_dataset = random_split(dataset, [80, 20])

train_loader = DataLoader(dataset=train_dataset, batch_size=9)
val_loader   = DataLoader(dataset=val_dataset, batch_size=9) 

n_epochs = 10

device = 'cuda' if torch.cuda.is_available() else 'cpu'

for epoch in range(n_epochs):
    print(f"epoch ##{epoch}")
    batch_no = 0
    for x_batch, y_batch in train_loader:
        print(f"train batch #{batch_no}, epoch #{epoch}")
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        print(x_batch,"\n",y_batch)
        batch_no += 1
    
    batch_no = 0    
    for x_val, y_val in val_loader:
        print(f"val batch #{batch_no}, epoch #{epoch}")
        x_val = x_val.to(device)
        y_val = y_val.to(device)
        print(x_val,"\n",y_val)
        batch_no += 1


'''
batch 의 값이 전체 dataset의 배수가 아니며 마지막 batch로 들어오는 크기는 줄어들 수 있음
epoch ##0
train batch #0, epoch #0
tensor([[0.3636, 0.9718, 0.9624],
        [0.5701, 0.0972, 0.6150],
        [0.7025, 0.3595, 0.2936],
        [0.3745, 0.9507, 0.7320],
        [0.3411, 0.1135, 0.9247],
        [0.8074, 0.8961, 0.3180],
        [0.2440, 0.9730, 0.3931],
        [0.0937, 0.3677, 0.2652],
        [0.2865, 0.5908, 0.0305]], device='cuda:0') 
 tensor([[1.6872],
        [1.1006],
        [1.2078],
        [1.5259],
        [1.0126],
        [1.5765],
        [1.1275],
        [1.1460],
        [1.0727]], device='cuda:0')
train batch #1, epoch #0

......

train batch #8, epoch #0
tensor([[0.5467, 0.1849, 0.9696],
        [0.5568, 0.9362, 0.6960],
        [0.7751, 0.9395, 0.8948],
        [0.8353, 0.3208, 0.1865],
        [0.1834, 0.3042, 0.5248],
        [0.3887, 0.2713, 0.8287],
        [0.9083, 0.2396, 0.1449],
        [0.6452, 0.1744, 0.6909]], device='cuda:0') 
 tensor([[1.3725],
        [1.6946],
        [2.3438],
        [1.1588],
        [1.0772],
        [1.3870],
        [1.2217],
        [1.1346]], device='cuda:0')
val batch #0, epoch #0
tensor([[0.5487, 0.6919, 0.6520],
        [0.6335, 0.5358, 0.0903],
        [0.1866, 0.8926, 0.5393],
        [0.2419, 0.0931, 0.8972],
        [0.3867, 0.9367, 0.1375],
        [0.5107, 0.4174, 0.2221],
        [0.7958, 0.8900, 0.3380],
        [0.6376, 0.8872, 0.4722],
        [0.8180, 0.8607, 0.0070]], device='cuda:0') 
 tensor([[1.5698],
        [1.0461],
        [1.0360],
        [0.9711],
        [1.0503],
        [1.1409],
        [1.3574],
        [1.5283],
        [0.9116]], device='cuda:0')
......
        
val batch #1, epoch #9
tensor([[0.3702, 0.0155, 0.9283],
        [0.2848, 0.0369, 0.6096],
        [0.8324, 0.2123, 0.1818],
        [0.4319, 0.2912, 0.6119],
        [0.5026, 0.5769, 0.4925],
        [0.0243, 0.6455, 0.1771],
        [0.8774, 0.7408, 0.6970],
        [0.6233, 0.3309, 0.0636],
        [0.7081, 0.0206, 0.9699]], device='cuda:0') 
 tensor([[1.0920],
        [1.0242],
        [0.8618],
        [1.0878],
        [1.2654],
        [1.1154],
        [1.9157],
        [1.1037],
        [1.0917]], device='cuda:0')
val batch #2, epoch #9
tensor([[0.5613, 0.7710, 0.4938],
        [0.8172, 0.5552, 0.5297]], device='cuda:0') 
 tensor([[1.3249],
        [1.5163]], device='cuda:0')

'''