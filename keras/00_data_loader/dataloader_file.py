from tensorflow.keras.utils import Sequence
import numpy as np
import math

batch_size = 9
lr = 1e-1
n_epochs = 5
train_data_ratio = 0.8


class CustomDataset:
    def __init__(self, x_tensor_filename, y_tensor_filename, base_idx=None, cnt=None):
        self.x_fn = x_tensor_filename
        self.y_fn = y_tensor_filename
        self.base_idx = base_idx
        self.cnt = cnt
        if self.base_idx is None:
            with open(y_tensor_filename, 'r') as fp:
                for count, line in enumerate(fp):
                    pass
            self.total_len = count + 1
        else:
            self.total_len = cnt

    def __getitem__(self, index):
        """
        주어진 인덱스 index 에 해당하는 샘플을 데이터셋에서 불러오고 반환합니다.
        """
        if self.base_idx is not None:
            index = index + self.base_idx
        x_data = np.loadtxt(self.x_fn, delimiter=',', skiprows=index, max_rows=1)
        # [0.37454012 0.95071431 0.73199394]
        if x_data.shape == ():
            x_data = np.array([x_data])
        y_data = np.loadtxt(self.y_fn, delimiter=',', skiprows=index, max_rows=1)
        # 1.5258549401766552
        if y_data.shape == ():
            y_data = np.array([y_data])
        # [1.5258549401766552]
        return x_data, y_data

    def __len__(self):
        """
        데이터셋의 샘플 개수를 반환합니다.
        """
        return self.total_len


class CustomDataloader(Sequence):
    def __init__(self, _dataset, batch_size=1, shuffle=False):
        self.dataset = _dataset
        self.batch_size = batch_size
        self.total_len = math.ceil(len(self.dataset) / self.batch_size)
        self.shuffle = shuffle
        self.indexer = np.arange(len(self.dataset))
        self.on_epoch_end()

    def __getitem__(self, index):
        indexer = self.indexer[index * self.batch_size:(index + 1) * self.batch_size]
        batch_x = [self.dataset[i][0] for i in indexer]
        batch_y = [self.dataset[i][1] for i in indexer]
        return np.array(batch_x), np.array(batch_y)

    def __len__(self):
        return self.total_len

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indexer)
            print("shuffle")


# temp_dataset 을 사용하는 이유는 전체 크기를 알기 위함입니다.
temp_dataset = CustomDataset("x_data.csv", "y_data.csv")
# 전체 dataset에서 train_dataset_cnt, val_dataset_cnt 갯수를 각각 분리
train_dataset_cnt = int(len(temp_dataset) * train_data_ratio)
val_dataset_cnt = len(temp_dataset) - train_dataset_cnt
# CustomDataset 인가 없으면 전체 dataset을 사용합니다. 여기에서는 정해진 크기까지만 사용하기 위해서 base_idx 시작 인덱스, cnt 전체크기 인자를 넘겼습니다.
train_dataset = CustomDataset("x_data.csv", "y_data.csv", 0, train_dataset_cnt)
val_dataset = CustomDataset("x_data.csv", "y_data.csv", train_dataset_cnt, val_dataset_cnt)
print(len(temp_dataset), train_dataset_cnt, val_dataset_cnt)
# CustomDataloader를 이용하면 한번에 batch_size 크기만큼 데이터가 올라오게 됩니다.
train_loader = CustomDataloader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = CustomDataloader(val_dataset, batch_size=batch_size, shuffle=True)


for epoch in range(n_epochs):
    print(f"epoch ##{epoch}")
    batch_no = 0
    for x_batch, y_batch in train_loader:
        print(f"train batch #{batch_no}, epoch #{epoch}, size {len(x_batch)}")
        print(x_batch, "\n", y_batch)
        batch_no += 1

"""
100 80 20
shuffle
shuffle
epoch ##0
train batch #0, epoch #0, size 9
[[0.66350177 0.00506158 0.16080805]
 [0.90826589 0.23956189 0.14489487]
 [0.35846573 0.11586906 0.86310343]
 [0.70807258 0.02058449 0.96990985]
 [0.30461377 0.09767211 0.68423303]
 [0.52273283 0.42754102 0.02541913]
 [0.89204656 0.63113863 0.7948113 ]
 [0.32320293 0.51879062 0.70301896]
 [0.08413996 0.16162871 0.89855419]] 
 [[0.945062  ]
 [1.22165584]
 [1.11608009]
 [1.09166539]
 [0.92068533]
 [0.98610501]
 [1.94967527]
 [1.17573523]
 [1.08740254]]
train batch #1, epoch #0, size 9
...
...
train batch #8, epoch #4, size 8
[[0.16122129 0.92969765 0.80812038]
 [0.11986537 0.33761517 0.9429097 ]
 [0.72821635 0.36778313 0.63230583]
 [0.48945276 0.98565045 0.24205527]
 [0.66252228 0.31171108 0.52006802]
 [0.5107473  0.417411   0.22210781]
 [0.18657006 0.892559   0.53934224]
 [0.94888554 0.96563203 0.80839735]] 
 [[1.25532762]
 [1.096222  ]
 [1.14348671]
 [1.10976758]
 [1.14947133]
 [1.14091336]
 [1.03604149]
 [2.5680029 ]]
"""