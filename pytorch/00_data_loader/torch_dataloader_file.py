import torch
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data.dataset import random_split


class CustomDataset(Dataset):
    def __init__(self, x_tensor_filename, y_tensor_filename):
        self.x_fn = x_tensor_filename
        self.y_fn = y_tensor_filename
        with open(y_tensor_filename, 'r') as fp:
            for count, line in enumerate(fp):
                pass
        self.total_len = count + 1
    def __getitem__(self, index):
        """
        주어진 인덱스 index 에 해당하는 샘플을 데이터셋에서 불러오고 반환합니다.
        """
        x_data = np.loadtxt(self.x_fn, delimiter=',', skiprows=index, max_rows=1)
        # [0.37454012 0.95071431 0.73199394]
        if x_data.shape==():
            x_data = np.array([x_data]) 
        y_data = np.loadtxt(self.y_fn, delimiter=',', skiprows=index, max_rows=1)
        # 1.5258549401766552
        if y_data.shape==():
            y_data = np.array([y_data]) 
        # [1.5258549401766552]
        return (x_data, y_data)
    def __len__(self):
        """
        데이터셋의 샘플 개수를 반환합니다.
        """
        return self.total_len
        
dataset = CustomDataset("x_data.csv", "y_data.csv")

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
tensor([[0.3492, 0.7260, 0.8971],
        [0.8074, 0.8961, 0.3180],
        [0.3745, 0.9507, 0.7320],
        [0.1271, 0.5222, 0.7700],
        [0.2848, 0.0369, 0.6096],
        [0.9132, 0.5113, 0.5015],
        [0.4895, 0.9857, 0.2421],
        [0.0408, 0.5909, 0.6776],
        [0.0359, 0.4656, 0.5426]], device='cuda:0', dtype=torch.float64) 
 tensor([[1.4856],
        [1.5765],
        [1.5259],
        [1.1010],
        [1.0242],
        [1.6776],
        [1.1098],
        [1.0607],
        [1.0973]], device='cuda:0', dtype=torch.float64)
train batch #1, epoch #0

......

'''