import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data.dataset import random_split
import matplotlib.pyplot as plt

batch_size = 100
lr = 1e-1
n_epochs = 5
device = 'cuda' if torch.cuda.is_available() else 'cpu'
train_data_ratio = 0.8

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
        x_data = np.loadtxt(self.x_fn, delimiter=',', dtype=float, skiprows=index, max_rows=1)
        # [0.37454012 0.95071431 0.73199394]
        if x_data.shape==():
            x_data = np.array([x_data]) 
        y_data = np.loadtxt(self.y_fn, delimiter=',', dtype=float, skiprows=index, max_rows=1)
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
train_dataset_cnt = int(len(dataset)*train_data_ratio)
val_dataset_cnt = len(dataset) - train_dataset_cnt
train_dataset, val_dataset = random_split(dataset, [train_dataset_cnt, val_dataset_cnt])

train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size)
val_loader   = DataLoader(dataset=val_dataset, batch_size=batch_size) 


class CustomModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.main = nn.Sequential(
            nn.Linear(3, 6),
            nn.Linear(6, 1)
        )
                
    def forward(self, x):
        return self.main(x)


def make_train_step(model, loss_fn, optimizer):
    # Builds function that performs a step in the train loop
    def train_step(x, y):
        # Sets model to TRAIN mode
        model.train()
        # Makes predictions
        yhat = model(x)
        # Computes loss
        loss = loss_fn(y, yhat)
        # zeroes gradients
        optimizer.zero_grad()
        # Computes gradients
        loss.backward()
        # Updates parameters
        optimizer.step()
        # Returns the loss
        return loss.item()
    
    # Returns the function that will be called inside the train loop
    return train_step


if __name__ == '__main__':
    model = CustomModel().to(device)
    loss_fn = nn.MSELoss(reduction='mean')
    print(model.parameters())
    optimizer = optim.SGD(model.parameters(), lr=lr)

    # Creates the train_step function for our model, loss function and optimizer
    train_step = make_train_step(model, loss_fn, optimizer)
    losses = []
    val_losses = []

    for epoch in range(n_epochs):
        print(f"epoch ##{epoch}")
        for x_batch, y_batch in train_loader:
            x_batch = x_batch.float()
            y_batch = y_batch.float()
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)
            loss = train_step(x_batch, y_batch)
            losses.append(loss)

        with torch.no_grad():
            for x_val, y_val in val_loader:
                x_val = x_val.float()
                y_val = y_val.float()
                x_val = x_val.to(device)
                y_val = y_val.to(device)

                model.eval()

                yhat = model(x_val)
                val_loss = loss_fn(y_val, yhat)
                val_losses.append(val_loss.item())

    torch.save(model.state_dict(), "model.pt")

    print(model.state_dict())

    fig, ax = plt.subplots()
    ax.plot(losses)
    ax.plot(val_losses)
    plt.savefig("losses.png")

    # test
    model.eval()
    x_prd = np.array([0.1, 0.2, 0.1]) # y = 1 + 2*0.1*0.2*0.1
    print("expect:",1 + 2*0.1*0.2*0.1)
    x_prd = torch.from_numpy(x_prd)
    x_prd = x_prd.float()
    x_prd = x_prd.to(device)
    print(model(x_prd))
    # y는 원하는 값 목표값인 label로 표현합니다.
    # 아래 방정식은 모르는 상태에서 학습을 통해 알아내는 것이 머신러닝이다.
