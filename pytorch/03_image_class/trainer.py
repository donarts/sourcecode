import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import os
from torchvision import transforms
from PIL import Image
from torchinfo import summary

batch_size = 20
lr = 1e-3
n_epochs = 200
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# 학습 과정에 문제가 발생하는 경우 중지시킨다
torch.autograd.set_detect_anomaly(True)


# fig = plt.gcf()


class CustomDataset(Dataset):
    def __init__(self, base_path, transform=None, target_transform=None):
        self.base_dir = base_path
        self.transform = transform
        self.target_transform = target_transform
        # 훈련에 사용되는 고양이/개 이미지 경로
        self.cats_dir = os.path.join(self.base_dir, 'cats')
        self.dogs_dir = os.path.join(self.base_dir, 'dogs')
        '''
        cats_and_dogs_filtered/train/cats
        cats_and_dogs_filtered/train/dogs
        cats_and_dogs_filtered/validation/cats
        cats_and_dogs_filtered/validation/dogs
        '''
        # os.listdir() 경로 내에 있는 파일의 이름을 리스트의 형태로 반환합니다.
        # [...'cat.102.jpg', 'cat.103.jpg', .... ]
        self.cat_fnames = os.listdir(self.cats_dir)
        self.dog_fnames = os.listdir(self.dogs_dir)

        self.total_len = len(self.cat_fnames) + len(self.dog_fnames)
        print(f"total images:{self.total_len}")

    def __getitem__(self, index):
        """
        주어진 인덱스 index 에 해당하는 샘플을 데이터셋에서 불러오고 반환합니다.
        cat[xxx]
        cat[xxx]
        dog[xxx]
        dog[xxx]
        """
        if index >= len(self.cat_fnames):
            # dog
            x_data = self.dog_fnames[index - len(self.cat_fnames)]
            y_data = np.array([0.0, 1.0])
            img_path = os.path.join(self.dogs_dir, x_data)
            image = Image.open(img_path)
            # plt.imshow(image)
            # print(y_data)
            # plt.show()
        else:
            # cat
            x_data = self.cat_fnames[index]
            y_data = np.array([1.0, 0.0])
            img_path = os.path.join(self.cats_dir, x_data)
            image = Image.open(img_path)
            # plt.imshow(image)
            # print(y_data)
            # plt.show()

        if self.transform:
            image = self.transform(image)
            # plt.imshow(image)
            # plt.show()

        if self.target_transform:
            y_data = self.target_transform(y_data)
        return image, y_data

    def __len__(self):
        """
        데이터셋의 샘플 개수를 반환합니다.
        """
        return self.total_len


# https://pytorch.org/vision/stable/auto_examples/plot_transforms.html#sphx-glr-auto-examples-plot-transforms-py
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomVerticalFlip(),
        transforms.RandomHorizontalFlip(),
        transforms.RandomResizedCrop(150),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ]),
    'validation': transforms.Compose([
        transforms.Resize(150),
        transforms.CenterCrop(150),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ]),
}

train_dataset = CustomDataset("cats_and_dogs_filtered/train", transform=data_transforms['train'])
val_dataset = CustomDataset("cats_and_dogs_filtered/validation", transform=data_transforms['validation'])

train_loader = DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(dataset=val_dataset, batch_size=batch_size, shuffle=True)


class CustomModel(nn.Module):
    def __init__(self):
        super().__init__()
        # https://pytorch.org/docs/stable/nn.html
        self.main = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(8, 8),
            nn.Flatten(),
            nn.Linear(5184, 512),
            nn.ReLU(),
            nn.Linear(512, 2),
            nn.ReLU(),
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
        # print("yhat",yhat)
        # print("y", y)
        loss = loss_fn(yhat, y)
        # zeroes gradients
        optimizer.zero_grad()
        # Computes gradients
        loss.backward()
        # Updates parameters
        optimizer.step()
        # Returns the loss
        # print("loss",loss)
        return loss.item()

    # Returns the function that will be called inside the train loop
    return train_step


model = CustomModel().to(device)
"""
https://pytorch.org/docs/stable/nn.html#loss-functions
"""
loss_fn = nn.L1Loss()
"""
https://pytorch.org/docs/stable/optim.html
"""
optimizer = optim.SGD(model.parameters(), lr=lr)

print(model.parameters())
print(model)

if __name__ == '__main__':
    train_step = make_train_step(model, loss_fn, optimizer)
    losses = []
    val_losses = []
    summary(model, input_size=(batch_size, 3, 150, 150))

    for epoch in range(n_epochs):
        epoch_loss = 0.0
        epoch_val_loss = 0.0
        print(f"epoch ##{epoch}")
        for x_batch, y_batch in train_loader:
            # print(x_batch.shape)
            # print(x_batch,y_batch)
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)
            epoch_loss += train_step(x_batch, y_batch)
        losses.append(epoch_loss)

        with torch.no_grad():
            for x_val, y_val in val_loader:
                x_val = x_val.to(device)
                y_val = y_val.to(device)

                model.eval()

                yhat = model(x_val)
                loss_f_ret = loss_fn(y_val, yhat)
                epoch_val_loss += loss_f_ret.item()
            val_losses.append(epoch_val_loss)
            print("yhat", yhat)
            print("y", y_val)
        print(f"epoch_loss:{epoch_loss} epoch_val_loss:{epoch_val_loss}")

    torch.save(model.state_dict(), "model.pt")
    print(model.state_dict())

    fig, ax = plt.subplots()
    ax.plot(losses)
    ax.plot(val_losses)
    plt.savefig("losses.png")
