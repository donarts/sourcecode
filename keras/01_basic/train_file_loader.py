from tensorflow import keras
from tensorflow.keras.utils import Sequence
from tensorflow.keras import layers
import tensorflow as tf
import numpy as np
import math

batch_size = 100
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


temp_dataset = CustomDataset("x_data.csv", "y_data.csv")
train_dataset_cnt = int(len(temp_dataset) * train_data_ratio)
val_dataset_cnt = len(temp_dataset) - train_dataset_cnt
train_dataset = CustomDataset("x_data.csv", "y_data.csv", 0, train_dataset_cnt)
val_dataset = CustomDataset("x_data.csv", "y_data.csv", train_dataset_cnt, val_dataset_cnt)
print(len(temp_dataset), train_dataset_cnt, val_dataset_cnt)
train_loader = CustomDataloader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = CustomDataloader(val_dataset, batch_size=batch_size, shuffle=True)

# https://keras.io/api/layers/
inputs = keras.Input(shape=(None, 3))
x = layers.Dense(6, activation="linear")(inputs)
x = layers.Dense(1, activation="linear")(x)
outputs = x
model = keras.Model(inputs, outputs)
model.summary()

# https://keras.io/api/optimizers/
# https://keras.io/api/losses/
INPUT_OPTIMIZER = tf.keras.optimizers.SGD(learning_rate=lr)
LOSS = tf.keras.losses.MeanSquaredError(reduction="auto", name="mean_squared_error")
model.compile(optimizer=INPUT_OPTIMIZER, loss=LOSS)
model.fit(train_loader, batch_size=batch_size, epochs=n_epochs, validation_data=val_loader)



# y = 1 + 2*0.1*0.2*0.1
x_prd = np.array([[0.1, 0.2, 0.1]])
print("expect:", 1 + 2 * 0.1 * 0.2 * 0.1)
print(model.predict(x_prd))

"""
5000 4000 1000
shuffle
shuffle
Model: "model"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input_1 (InputLayer)        [(None, None, 3)]         0         
                                                                 
 dense (Dense)               (None, None, 6)           24        
                                                                 
 dense_1 (Dense)             (None, None, 1)           7         
                                                                 
=================================================================
Total params: 31
Trainable params: 31
Non-trainable params: 0
_________________________________________________________________
Epoch 1/5
WARNING:tensorflow:Model was constructed with shape (None, None, 3) for input KerasTensor(type_spec=TensorSpec(shape=(None, None, 3), dtype=tf.float32, name='input_1'), name='input_1', description="created by layer 'input_1'"), but it was called on an input with incompatible shape (None, None).
WARNING:tensorflow:Model was constructed with shape (None, None, 3) for input KerasTensor(type_spec=TensorSpec(shape=(None, None, 3), dtype=tf.float32, name='input_1'), name='input_1', description="created by layer 'input_1'"), but it was called on an input with incompatible shape (None, None).
40/40 [==============================] - ETA: 0s - loss: 0.2153WARNING:tensorflow:Model was constructed with shape (None, None, 3) for input KerasTensor(type_spec=TensorSpec(shape=(None, None, 3), dtype=tf.float32, name='input_1'), name='input_1', description="created by layer 'input_1'"), but it was called on an input with incompatible shape (None, None).
shuffle
40/40 [==============================] - 11s 269ms/step - loss: 0.2153 - val_loss: 0.0621
shuffle
Epoch 2/5
40/40 [==============================] - ETA: 0s - loss: 0.0514shuffle
40/40 [==============================] - 10s 260ms/step - loss: 0.0514 - val_loss: 0.0423
shuffle
Epoch 3/5
40/40 [==============================] - ETA: 0s - loss: 0.0393shuffle
40/40 [==============================] - 10s 260ms/step - loss: 0.0393 - val_loss: 0.0365
shuffle
Epoch 4/5
40/40 [==============================] - ETA: 0s - loss: 0.0355shuffle
40/40 [==============================] - 10s 264ms/step - loss: 0.0355 - val_loss: 0.0337
shuffle
Epoch 5/5
40/40 [==============================] - ETA: 0s - loss: 0.0339shuffle
40/40 [==============================] - 10s 255ms/step - loss: 0.0339 - val_loss: 0.0324
shuffle
expect: 1.004
WARNING:tensorflow:Model was constructed with shape (None, None, 3) for input KerasTensor(type_spec=TensorSpec(shape=(None, None, 3), dtype=tf.float32, name='input_1'), name='input_1', description="created by layer 'input_1'"), but it was called on an input with incompatible shape (None, 3).
1/1 [==============================] - 0s 41ms/step
[[0.7554034]]
"""