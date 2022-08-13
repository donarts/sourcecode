from tensorflow import keras
from tensorflow.keras.utils import Sequence
from tensorflow.keras import layers
import tensorflow as tf
import numpy as np
import math

batch_size = 100
lr = 1e-3
n_epochs = 50
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
        x_data = np.loadtxt(self.x_fn, delimiter=',', skiprows=0, max_rows=1)
        self.feature_cnt = len(x_data)

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
        # x_data [5.          5.00999946 5.0199977 5.02999448 5.03998959] y_data [2.40299196]
        x_data = np.reshape(x_data, (-1, 1))
        # x_data [[5.        ][5.00999946][5.0199977 ][5.02999448][5.03998959]] y_data [2.40299196]
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
        #[[5.         5.00999946 5.0199977  5.02999448 5.03998959]
        # [5.00999946 5.0199977  5.02999448 5.03998959 5.04998279]
        # ...
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
inputs = keras.Input(shape=(5, 1))
x = layers.SimpleRNN(6)(inputs)
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
model.save("model_rnn.keras")

"""
14395 11516 2879
2022-08-13 18:23:59.001158: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cusolver64_11.dll'; dlerror: cusolver64_11.dll not found
2022-08-13 18:23:59.003608: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudnn64_8.dll'; dlerror: cudnn64_8.dll not found
2022-08-13 18:23:59.003760: W tensorflow/core/common_runtime/gpu/gpu_device.cc:1850] Cannot dlopen some GPU libraries. Please make sure the missing libraries mentioned above are installed properly if you would like to use GPU. Follow the guide at https://www.tensorflow.org/install/gpu for how to download and setup the required libraries for your platform.
Skipping registering GPU devices...
2022-08-13 18:23:59.004247: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX AVX2
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
Model: "model"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input_1 (InputLayer)        [(None, 5, 1)]            0         
                                                                 
 simple_rnn (SimpleRNN)      (None, 6)                 48        
                                                                 
 dense (Dense)               (None, 1)                 7         
                                                                 
=================================================================
Total params: 55
Trainable params: 55
Non-trainable params: 0
_________________________________________________________________
Epoch 1/50
116/116 [==============================] - 101s 874ms/step - loss: 3.7985 - val_loss: 4.1360
Epoch 2/50
116/116 [==============================] - 99s 853ms/step - loss: 1.7602 - val_loss: 2.4225
Epoch 3/50
116/116 [==============================] - 99s 857ms/step - loss: 1.0908 - val_loss: 1.5594
Epoch 4/50
116/116 [==============================] - 101s 872ms/step - loss: 0.6845 - val_loss: 0.9763
Epoch 5/50
116/116 [==============================] - 100s 864ms/step - loss: 0.4588 - val_loss: 0.6872
Epoch 6/50
116/116 [==============================] - 110s 954ms/step - loss: 0.3262 - val_loss: 0.4753
Epoch 7/50
116/116 [==============================] - 116s 1s/step - loss: 0.2494 - val_loss: 0.3548
Epoch 8/50
116/116 [==============================] - 107s 926ms/step - loss: 0.1984 - val_loss: 0.2714
Epoch 9/50
116/116 [==============================] - 109s 939ms/step - loss: 0.1632 - val_loss: 0.2266
Epoch 10/50
116/116 [==============================] - 106s 922ms/step - loss: 0.1373 - val_loss: 0.1841
Epoch 11/50
116/116 [==============================] - 112s 974ms/step - loss: 0.1157 - val_loss: 0.1762
Epoch 12/50
116/116 [==============================] - 111s 960ms/step - loss: 0.1002 - val_loss: 0.1350
Epoch 13/50
116/116 [==============================] - 114s 986ms/step - loss: 0.0866 - val_loss: 0.1165
Epoch 14/50
116/116 [==============================] - 106s 916ms/step - loss: 0.0768 - val_loss: 0.1015
Epoch 15/50
116/116 [==============================] - 104s 899ms/step - loss: 0.0673 - val_loss: 0.0911
Epoch 16/50
116/116 [==============================] - 106s 917ms/step - loss: 0.0598 - val_loss: 0.0920
Epoch 17/50
116/116 [==============================] - 105s 908ms/step - loss: 0.0517 - val_loss: 0.0738
Epoch 18/50
116/116 [==============================] - 105s 908ms/step - loss: 0.0471 - val_loss: 0.0676
Epoch 19/50
116/116 [==============================] - 107s 925ms/step - loss: 0.0435 - val_loss: 0.0622
Epoch 20/50
116/116 [==============================] - 123s 1s/step - loss: 0.0403 - val_loss: 0.0588
Epoch 21/50
116/116 [==============================] - 120s 1s/step - loss: 0.0368 - val_loss: 0.0545
Epoch 22/50
116/116 [==============================] - 111s 950ms/step - loss: 0.0339 - val_loss: 0.0522
Epoch 23/50
116/116 [==============================] - 118s 1s/step - loss: 0.0314 - val_loss: 0.0470
Epoch 24/50
116/116 [==============================] - 110s 952ms/step - loss: 0.0283 - val_loss: 0.0441
Epoch 25/50
116/116 [==============================] - 122s 1s/step - loss: 0.0273 - val_loss: 0.0447
Epoch 26/50
116/116 [==============================] - 123s 1s/step - loss: 0.0250 - val_loss: 0.0430
Epoch 27/50
116/116 [==============================] - 108s 930ms/step - loss: 0.0242 - val_loss: 0.0389
Epoch 28/50
116/116 [==============================] - 105s 907ms/step - loss: 0.0228 - val_loss: 0.0366
Epoch 29/50
116/116 [==============================] - 105s 906ms/step - loss: 0.0222 - val_loss: 0.0382
Epoch 30/50
116/116 [==============================] - 105s 910ms/step - loss: 0.0206 - val_loss: 0.0344
Epoch 31/50
116/116 [==============================] - 106s 921ms/step - loss: 0.0201 - val_loss: 0.0336
Epoch 32/50
116/116 [==============================] - 106s 916ms/step - loss: 0.0196 - val_loss: 0.0320
Epoch 33/50
116/116 [==============================] - 105s 912ms/step - loss: 0.0177 - val_loss: 0.0337
Epoch 34/50
116/116 [==============================] - 106s 916ms/step - loss: 0.0183 - val_loss: 0.0305
Epoch 35/50
116/116 [==============================] - 105s 909ms/step - loss: 0.0176 - val_loss: 0.0280
Epoch 36/50
116/116 [==============================] - 106s 917ms/step - loss: 0.0172 - val_loss: 0.0305
Epoch 37/50
116/116 [==============================] - 111s 955ms/step - loss: 0.0166 - val_loss: 0.0265
Epoch 38/50
116/116 [==============================] - 113s 977ms/step - loss: 0.0163 - val_loss: 0.0264
Epoch 39/50
116/116 [==============================] - 116s 1s/step - loss: 0.0153 - val_loss: 0.0275
Epoch 40/50
116/116 [==============================] - 115s 989ms/step - loss: 0.0156 - val_loss: 0.0249
Epoch 41/50
116/116 [==============================] - 118s 1s/step - loss: 0.0154 - val_loss: 0.0238
Epoch 42/50
116/116 [==============================] - 121s 1s/step - loss: 0.0147 - val_loss: 0.0232
Epoch 43/50
116/116 [==============================] - 110s 944ms/step - loss: 0.0141 - val_loss: 0.0266
Epoch 44/50
116/116 [==============================] - 123s 1s/step - loss: 0.0146 - val_loss: 0.0239
Epoch 45/50
116/116 [==============================] - 105s 906ms/step - loss: 0.0139 - val_loss: 0.0232
Epoch 46/50
116/116 [==============================] - 107s 925ms/step - loss: 0.0136 - val_loss: 0.0215
Epoch 47/50
116/116 [==============================] - 120s 1s/step - loss: 0.0134 - val_loss: 0.0211
Epoch 48/50
116/116 [==============================] - 148s 1s/step - loss: 0.0129 - val_loss: 0.0214
Epoch 49/50
116/116 [==============================] - 131s 1s/step - loss: 0.0127 - val_loss: 0.0200
Epoch 50/50
116/116 [==============================] - 104s 901ms/step - loss: 0.0126 - val_loss: 0.0208
"""