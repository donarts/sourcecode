from tensorflow import keras
from tensorflow.keras.utils import Sequence
from tensorflow.keras import layers
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
import numpy as np
import math
import pickle

with open('char_to_index.pickle', 'rb') as fr:
    char_to_index = pickle.load(fr)

with open('index_to_char.pickle', 'rb') as fr:
    index_to_char = pickle.load(fr)

batch_size = 20
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
            with open(y_tensor_filename, 'r', encoding='utf-8') as fp:
                for count, line in enumerate(fp):
                    pass
            self.total_len = count + 1
        else:
            self.total_len = cnt

        with open(x_tensor_filename, "r", encoding='utf-8') as f:
            self.x_data_lines = [line for line in f]
        with open(y_tensor_filename, "r", encoding='utf-8') as f:
            self.y_data_lines = [line for line in f]

    def __getitem__(self, index):
        """
        주어진 인덱스 index 에 해당하는 샘플을 데이터셋에서 불러오고 반환합니다.
        """
        if self.base_idx is not None:
            index = index + self.base_idx
        x_data = self.x_data_lines[index].replace("\n", "")
        #print(x_data)
        x_data = np.array([to_categorical(char_to_index[i], 85) for i in x_data])
        #print(x_data.shape)
        #print(x_data)
        y_data = self.y_data_lines[index].replace("\n", "")
        #print(y_data)
        y_data = to_categorical(char_to_index[y_data], 85)
        #print(y_data)
        #x_data = np.reshape(x_data, (-1, 85))
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


temp_dataset = CustomDataset("x_data.txt", "y_data.txt")
train_dataset_cnt = int(len(temp_dataset) * train_data_ratio)
val_dataset_cnt = len(temp_dataset) - train_dataset_cnt
train_dataset = CustomDataset("x_data.txt", "y_data.txt", 0, train_dataset_cnt)
val_dataset = CustomDataset("x_data.txt", "y_data.txt", train_dataset_cnt, val_dataset_cnt)
print(len(temp_dataset), train_dataset_cnt, val_dataset_cnt)
train_loader = CustomDataloader(train_dataset, batch_size=batch_size, shuffle=False)
val_loader = CustomDataloader(val_dataset, batch_size=batch_size, shuffle=False)

# https://keras.io/api/layers/
inputs = keras.Input(shape=(4, 85))
x = layers.LSTM(60)(inputs)
x = layers.Dense(85, activation='softmax')(x)
outputs = x
model = keras.Model(inputs, outputs)
model.summary()

# https://keras.io/api/optimizers/
# https://keras.io/api/losses/
INPUT_OPTIMIZER = tf.keras.optimizers.Adam(learning_rate=lr)
LOSS = tf.keras.losses.CategoricalCrossentropy()
model.compile(optimizer=INPUT_OPTIMIZER, loss=LOSS)
model.fit(train_loader, batch_size=batch_size, epochs=n_epochs, validation_data=val_loader)
model.save("model_lstm.keras")

'''
279 223 56
2022-08-20 10:23:36.576946: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cusolver64_11.dll'; dlerror: cusolver64_11.dll not found
2022-08-20 10:23:36.579645: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'cudnn64_8.dll'; dlerror: cudnn64_8.dll not found
2022-08-20 10:23:36.579850: W tensorflow/core/common_runtime/gpu/gpu_device.cc:1850] Cannot dlopen some GPU libraries. Please make sure the missing libraries mentioned above are installed properly if you would like to use GPU. Follow the guide at https://www.tensorflow.org/install/gpu for how to download and setup the required libraries for your platform.
Skipping registering GPU devices...
2022-08-20 10:23:36.580699: I tensorflow/core/platform/cpu_feature_guard.cc:193] This TensorFlow binary is optimized with oneAPI Deep Neural Network Library (oneDNN) to use the following CPU instructions in performance-critical operations:  AVX AVX2
To enable them in other operations, rebuild TensorFlow with the appropriate compiler flags.
Model: "model"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 input_1 (InputLayer)        [(None, 4, 85)]           0         
                                                                 
 lstm (LSTM)                 (None, 60)                35040     
                                                                 
 dense (Dense)               (None, 85)                5185      
                                                                 
=================================================================
Total params: 40,225
Trainable params: 40,225
Non-trainable params: 0
_________________________________________________________________
Epoch 1/50
12/12 [==============================] - 1s 23ms/step - loss: 4.4400 - val_loss: 4.4262
Epoch 2/50
12/12 [==============================] - 0s 4ms/step - loss: 4.4039 - val_loss: 4.3948
Epoch 3/50
12/12 [==============================] - 0s 4ms/step - loss: 4.3606 - val_loss: 4.3512
Epoch 4/50
12/12 [==============================] - 0s 4ms/step - loss: 4.2906 - val_loss: 4.2747
Epoch 5/50
12/12 [==============================] - 0s 4ms/step - loss: 4.1535 - val_loss: 4.1075
Epoch 6/50
12/12 [==============================] - 0s 4ms/step - loss: 3.8944 - val_loss: 3.8651
Epoch 7/50
12/12 [==============================] - 0s 4ms/step - loss: 3.7237 - val_loss: 3.8388
Epoch 8/50
12/12 [==============================] - 0s 4ms/step - loss: 3.6581 - val_loss: 3.7765
Epoch 9/50
12/12 [==============================] - 0s 4ms/step - loss: 3.5942 - val_loss: 3.7746
Epoch 10/50
12/12 [==============================] - 0s 4ms/step - loss: 3.5545 - val_loss: 3.7465
Epoch 11/50
12/12 [==============================] - 0s 4ms/step - loss: 3.5149 - val_loss: 3.7227
Epoch 12/50
12/12 [==============================] - 0s 4ms/step - loss: 3.4697 - val_loss: 3.7108
Epoch 13/50
12/12 [==============================] - 0s 4ms/step - loss: 3.4246 - val_loss: 3.6961
Epoch 14/50
12/12 [==============================] - 0s 4ms/step - loss: 3.3848 - val_loss: 3.6519
Epoch 15/50
12/12 [==============================] - 0s 3ms/step - loss: 3.3276 - val_loss: 3.6426
Epoch 16/50
12/12 [==============================] - 0s 3ms/step - loss: 3.2704 - val_loss: 3.5921
Epoch 17/50
12/12 [==============================] - 0s 4ms/step - loss: 3.2082 - val_loss: 3.5731
Epoch 18/50
12/12 [==============================] - 0s 4ms/step - loss: 3.1412 - val_loss: 3.5327
Epoch 19/50
12/12 [==============================] - 0s 4ms/step - loss: 3.0699 - val_loss: 3.4891
Epoch 20/50
12/12 [==============================] - 0s 4ms/step - loss: 2.9889 - val_loss: 3.4257
Epoch 21/50
12/12 [==============================] - 0s 4ms/step - loss: 2.9030 - val_loss: 3.3826
Epoch 22/50
12/12 [==============================] - 0s 4ms/step - loss: 2.8177 - val_loss: 3.3197
Epoch 23/50
12/12 [==============================] - 0s 4ms/step - loss: 2.7216 - val_loss: 3.2720
Epoch 24/50
12/12 [==============================] - 0s 4ms/step - loss: 2.6283 - val_loss: 3.2156
Epoch 25/50
12/12 [==============================] - 0s 4ms/step - loss: 2.5297 - val_loss: 3.1799
Epoch 26/50
12/12 [==============================] - 0s 4ms/step - loss: 2.4361 - val_loss: 3.1063
Epoch 27/50
12/12 [==============================] - 0s 4ms/step - loss: 2.3331 - val_loss: 3.0865
Epoch 28/50
12/12 [==============================] - 0s 4ms/step - loss: 2.2367 - val_loss: 3.0124
Epoch 29/50
12/12 [==============================] - 0s 4ms/step - loss: 2.1327 - val_loss: 2.9974
Epoch 30/50
12/12 [==============================] - 0s 4ms/step - loss: 2.0387 - val_loss: 2.9617
Epoch 31/50
12/12 [==============================] - 0s 4ms/step - loss: 1.9494 - val_loss: 2.9479
Epoch 32/50
12/12 [==============================] - 0s 3ms/step - loss: 1.8460 - val_loss: 2.9146
Epoch 33/50
12/12 [==============================] - 0s 4ms/step - loss: 1.7531 - val_loss: 2.9316
Epoch 34/50
12/12 [==============================] - 0s 4ms/step - loss: 1.6658 - val_loss: 2.8914
Epoch 35/50
12/12 [==============================] - 0s 4ms/step - loss: 1.5826 - val_loss: 2.9087
Epoch 36/50
12/12 [==============================] - 0s 4ms/step - loss: 1.5006 - val_loss: 2.9242
Epoch 37/50
12/12 [==============================] - 0s 4ms/step - loss: 1.4244 - val_loss: 2.9103
Epoch 38/50
12/12 [==============================] - 0s 4ms/step - loss: 1.3474 - val_loss: 2.9748
Epoch 39/50
12/12 [==============================] - 0s 4ms/step - loss: 1.2815 - val_loss: 2.9538
Epoch 40/50
12/12 [==============================] - 0s 3ms/step - loss: 1.2125 - val_loss: 3.0242
Epoch 41/50
12/12 [==============================] - 0s 3ms/step - loss: 1.1398 - val_loss: 2.9633
Epoch 42/50
12/12 [==============================] - 0s 4ms/step - loss: 1.0929 - val_loss: 3.0585
Epoch 43/50
12/12 [==============================] - 0s 4ms/step - loss: 1.0249 - val_loss: 3.0636
Epoch 44/50
12/12 [==============================] - 0s 4ms/step - loss: 0.9632 - val_loss: 3.0656
Epoch 45/50
12/12 [==============================] - 0s 4ms/step - loss: 0.9112 - val_loss: 3.0943
Epoch 46/50
12/12 [==============================] - 0s 4ms/step - loss: 0.8600 - val_loss: 3.0998
Epoch 47/50
12/12 [==============================] - 0s 3ms/step - loss: 0.8218 - val_loss: 3.1171
Epoch 48/50
12/12 [==============================] - 0s 4ms/step - loss: 0.7693 - val_loss: 3.1759
Epoch 49/50
12/12 [==============================] - 0s 4ms/step - loss: 0.7254 - val_loss: 3.1406
Epoch 50/50
12/12 [==============================] - 0s 4ms/step - loss: 0.6885 - val_loss: 3.1862
'''