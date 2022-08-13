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
x = layers.LSTM(6)(inputs)
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
model.save("model_lstm.keras")

"""
14395 11516 2879
2022-08-13 19:57:08.106716: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cusolver64_11.dll'; dlerror: cusolver64_11.dll not found
2022-08-13 19:57:08.109881: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudnn64_8.dll'; dlerror: cudnn64_8.dll not found
2022-08-13 19:57:08.110032: W tensorflow/core/common_runtime/gpu/gpu_device.cc:1850] Cannot dlopen some GPU libraries. Please make sure the missing libraries mentioned above are installed properly if you would like to use GPU. Follow the guide at https://www.tensorflow.org/install/gpu for how to download and setup the required libraries for your platform.
Skipping registering GPU devices...
2022-08-13 19:57:08.110536: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX AVX2
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
Model: "model"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input_1 (InputLayer)        [(None, 5, 1)]            0         
                                                                 
 lstm (LSTM)                 (None, 6)                 192       
                                                                 
 dense (Dense)               (None, 1)                 7         
                                                                 
=================================================================
Total params: 199
Trainable params: 199
Non-trainable params: 0
_________________________________________________________________
Epoch 1/50
116/116 [==============================] - 103s 881ms/step - loss: 15.5924 - val_loss: 17.7455
Epoch 2/50
116/116 [==============================] - 101s 866ms/step - loss: 7.9232 - val_loss: 10.4694
Epoch 3/50
116/116 [==============================] - 101s 868ms/step - loss: 4.7581 - val_loss: 7.0017
Epoch 4/50
116/116 [==============================] - 105s 906ms/step - loss: 3.2727 - val_loss: 4.7020
Epoch 5/50
116/116 [==============================] - 100s 864ms/step - loss: 2.3602 - val_loss: 3.4468
Epoch 6/50
116/116 [==============================] - 101s 875ms/step - loss: 1.6608 - val_loss: 2.5458
Epoch 7/50
116/116 [==============================] - 100s 867ms/step - loss: 1.2068 - val_loss: 1.8406
Epoch 8/50
116/116 [==============================] - 100s 857ms/step - loss: 0.8749 - val_loss: 1.3899
Epoch 9/50
116/116 [==============================] - 100s 870ms/step - loss: 0.6390 - val_loss: 1.0374
Epoch 10/50
116/116 [==============================] - 100s 866ms/step - loss: 0.4795 - val_loss: 0.8041
Epoch 11/50
116/116 [==============================] - 100s 861ms/step - loss: 0.3785 - val_loss: 0.6039
Epoch 12/50
116/116 [==============================] - 100s 864ms/step - loss: 0.3114 - val_loss: 0.5255
Epoch 13/50
116/116 [==============================] - 280s 2s/step - loss: 0.2590 - val_loss: 0.3964
Epoch 14/50
116/116 [==============================] - 144s 1s/step - loss: 0.2235 - val_loss: 0.3893
Epoch 15/50
116/116 [==============================] - 188s 2s/step - loss: 0.1902 - val_loss: 0.2887
Epoch 16/50
116/116 [==============================] - 171s 1s/step - loss: 0.1732 - val_loss: 0.2438
Epoch 17/50
116/116 [==============================] - 200s 2s/step - loss: 0.1531 - val_loss: 0.2405
Epoch 18/50
116/116 [==============================] - 193s 2s/step - loss: 0.1408 - val_loss: 0.2095
Epoch 19/50
116/116 [==============================] - 197s 2s/step - loss: 0.1414 - val_loss: 0.1676
Epoch 20/50
116/116 [==============================] - 200s 2s/step - loss: 0.1213 - val_loss: 0.1878
Epoch 21/50
116/116 [==============================] - 189s 2s/step - loss: 0.1121 - val_loss: 0.1420
Epoch 22/50
116/116 [==============================] - 193s 2s/step - loss: 0.1064 - val_loss: 0.1272
Epoch 23/50
116/116 [==============================] - 182s 2s/step - loss: 0.1010 - val_loss: 0.1510
Epoch 24/50
116/116 [==============================] - 184s 2s/step - loss: 0.0933 - val_loss: 0.1173
Epoch 25/50
116/116 [==============================] - 188s 2s/step - loss: 0.0846 - val_loss: 0.1362
Epoch 26/50
116/116 [==============================] - 188s 2s/step - loss: 0.0880 - val_loss: 0.0957
Epoch 27/50
116/116 [==============================] - 188s 2s/step - loss: 0.0805 - val_loss: 0.0968
Epoch 28/50
116/116 [==============================] - 176s 2s/step - loss: 0.0737 - val_loss: 0.0841
Epoch 29/50
116/116 [==============================] - 172s 1s/step - loss: 0.0673 - val_loss: 0.0864
Epoch 30/50
116/116 [==============================] - 178s 2s/step - loss: 0.0676 - val_loss: 0.0973
Epoch 31/50
116/116 [==============================] - 189s 2s/step - loss: 0.0691 - val_loss: 0.0754
Epoch 32/50
116/116 [==============================] - 183s 2s/step - loss: 0.0629 - val_loss: 0.1238
Epoch 33/50
116/116 [==============================] - 108s 927ms/step - loss: 0.0540 - val_loss: 0.0775
Epoch 34/50
116/116 [==============================] - 101s 876ms/step - loss: 0.0544 - val_loss: 0.0622
Epoch 35/50
116/116 [==============================] - 101s 872ms/step - loss: 0.0544 - val_loss: 0.0592
Epoch 36/50
116/116 [==============================] - 101s 872ms/step - loss: 0.0551 - val_loss: 0.0563
Epoch 37/50
116/116 [==============================] - 102s 884ms/step - loss: 0.0483 - val_loss: 0.0756
Epoch 38/50
116/116 [==============================] - 100s 859ms/step - loss: 0.0475 - val_loss: 0.0695
Epoch 39/50
116/116 [==============================] - 101s 873ms/step - loss: 0.0465 - val_loss: 0.0647
Epoch 40/50
116/116 [==============================] - 102s 877ms/step - loss: 0.0432 - val_loss: 0.0691
Epoch 41/50
116/116 [==============================] - 100s 864ms/step - loss: 0.0389 - val_loss: 0.0686
Epoch 42/50
116/116 [==============================] - 100s 859ms/step - loss: 0.0349 - val_loss: 0.0436
Epoch 43/50
116/116 [==============================] - 99s 860ms/step - loss: 0.0355 - val_loss: 0.0415
Epoch 44/50
116/116 [==============================] - 100s 862ms/step - loss: 0.0393 - val_loss: 0.0406
Epoch 45/50
116/116 [==============================] - 100s 865ms/step - loss: 0.0363 - val_loss: 0.0444
Epoch 46/50
116/116 [==============================] - 100s 869ms/step - loss: 0.0335 - val_loss: 0.0374
Epoch 47/50
116/116 [==============================] - 100s 863ms/step - loss: 0.0307 - val_loss: 0.0374
Epoch 48/50
116/116 [==============================] - 99s 858ms/step - loss: 0.0313 - val_loss: 0.0382
Epoch 49/50
116/116 [==============================] - 100s 861ms/step - loss: 0.0296 - val_loss: 0.0507
Epoch 50/50
116/116 [==============================] - 100s 865ms/step - loss: 0.0300 - val_loss: 0.0337
"""