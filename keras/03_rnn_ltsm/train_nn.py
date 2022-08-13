from tensorflow import keras
from tensorflow.keras.utils import Sequence
from tensorflow.keras import layers
import tensorflow as tf
import numpy as np
import math

batch_size = 100
lr = 1e-3
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
train_loader = CustomDataloader(train_dataset, batch_size=batch_size, shuffle=False)
val_loader = CustomDataloader(val_dataset, batch_size=batch_size, shuffle=False)

# https://keras.io/api/layers/
inputs = keras.Input(shape=(None, 5))
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
model.save("model_nn.keras")



"""
14395 11516 2879
shuffle
shuffle
2022-08-13 11:30:05.583930: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cusolver64_11.dll'; dlerror: cusolver64_11.dll not found
2022-08-13 11:30:05.586539: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudnn64_8.dll'; dlerror: cudnn64_8.dll not found
2022-08-13 11:30:05.586690: W tensorflow/core/common_runtime/gpu/gpu_device.cc:1850] Cannot dlopen some GPU libraries. Please make sure the missing libraries mentioned above are installed properly if you would like to use GPU. Follow the guide at https://www.tensorflow.org/install/gpu for how to download and setup the required libraries for your platform.
Skipping registering GPU devices...
2022-08-13 11:30:05.587207: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX AVX2
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
Model: "model"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input_1 (InputLayer)        [(None, None, 5)]         0         
                                                                 
 dense (Dense)               (None, None, 6)           36        
                                                                 
 dense_1 (Dense)             (None, None, 1)           7         
                                                                 
=================================================================
Total params: 43
Trainable params: 43
Non-trainable params: 0
_________________________________________________________________
Epoch 1/5
WARNING:tensorflow:Model was constructed with shape (None, None, 5) for input KerasTensor(type_spec=TensorSpec(shape=(None, None, 5), dtype=tf.float32, name='input_1'), name='input_1', description="created by layer 'input_1'"), but it was called on an input with incompatible shape (None, None).
WARNING:tensorflow:Model was constructed with shape (None, None, 5) for input KerasTensor(type_spec=TensorSpec(shape=(None, None, 5), dtype=tf.float32, name='input_1'), name='input_1', description="created by layer 'input_1'"), but it was called on an input with incompatible shape (None, None).
116/116 [==============================] - ETA: 0s - loss: 0.4643WARNING:tensorflow:Model was constructed with shape (None, None, 5) for input KerasTensor(type_spec=TensorSpec(shape=(None, None, 5), dtype=tf.float32, name='input_1'), name='input_1', description="created by layer 'input_1'"), but it was called on an input with incompatible shape (None, None).
shuffle
116/116 [==============================] - 99s 856ms/step - loss: 0.4643 - val_loss: 9.9400e-04
shuffle
Epoch 2/5
116/116 [==============================] - ETA: 0s - loss: 9.4903e-04shuffle
116/116 [==============================] - 98s 850ms/step - loss: 9.4903e-04 - val_loss: 9.0000e-04
shuffle
Epoch 3/5
116/116 [==============================] - ETA: 0s - loss: 9.1738e-04shuffle
116/116 [==============================] - 98s 848ms/step - loss: 9.1738e-04 - val_loss: 0.0010
shuffle
Epoch 4/5
116/116 [==============================] - ETA: 0s - loss: 8.9068e-04shuffle
116/116 [==============================] - 99s 852ms/step - loss: 8.9068e-04 - val_loss: 9.9437e-04
shuffle
Epoch 5/5
116/116 [==============================] - ETA: 0s - loss: 8.6808e-04shuffle
116/116 [==============================] - 98s 851ms/step - loss: 8.6808e-04 - val_loss: 9.2219e-04
shuffle
"""