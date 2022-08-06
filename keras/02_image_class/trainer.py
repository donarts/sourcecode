from tensorflow import keras
from tensorflow.keras.utils import Sequence
from tensorflow.keras import layers
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import math

batch_size = 20
lr = 1e-3
n_epochs = 20
IMG_SIZE = 150

# fig = plt.gcf()


class CustomDataset:
    def __init__(self, base_path, transform=None, target_transform=None, base_idx=None, cnt=None, file_name=None):
        self.file_name = None
        self.base_idx = base_idx
        self.cnt = cnt
        self.base_dir = base_path
        self.transform = transform
        self.cat_fnames = []
        self.dog_fnames = []
        self.target_transform = target_transform
        # 훈련에 사용되는 고양이/개 이미지 경로
        self.cats_dir = os.path.join(self.base_dir, 'cats')
        self.dogs_dir = os.path.join(self.base_dir, 'dogs')
        if file_name is not None:
            self.file_name = file_name
            self.total_len = 1
            return
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
        if self.base_idx is None:
            self.total_len = len(self.cat_fnames) + len(self.dog_fnames)
        else:
            self.total_len = cnt

        print(f"total images:{self.total_len}")

    def __getitem__(self, index):
        """
        주어진 인덱스 index 에 해당하는 샘플을 데이터셋에서 불러오고 반환합니다.
        cat[xxx]
        cat[xxx]
        dog[xxx]
        dog[xxx]
        """
        if self.base_idx is not None:
            index = index + self.base_idx

        if self.file_name is not None:
            y_data = np.array([0.0, 1.0])
            image = Image.open(self.file_name)
        elif index >= len(self.cat_fnames):
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
            image = tf.keras.preprocessing.image.img_to_array(image)
            image = image.astype('float32')
            image /= 255.0
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
        batch_x = np.array(batch_x)
        batch_y = np.array(batch_y)
        return batch_x, batch_y

    def __len__(self):
        return self.total_len

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.indexer)


"""
# https://keras.io/api/layers/preprocessing_layers/image_augmentation/
https://www.tensorflow.org/tutorials/images/data_augmentation?hl=ko
참고: data_augmentation 데이터 증강은 테스트할 때 비활성화되므로 입력 이미지는 model.fit(model.evaluate 또는 model.predict가 아님) 호출 중에만 증강됩니다.
RandomCrop layer
RandomFlip layer
RandomTranslation layer
RandomRotation layer
RandomZoom layer
RandomHeight layer
RandomWidth layer
RandomContrast layer
RandomBrightness layer
"""


val_processing = tf.keras.Sequential([
    layers.Resizing(IMG_SIZE, IMG_SIZE),
    layers.CenterCrop(IMG_SIZE, IMG_SIZE),
    layers.Normalization(mean=[0.485, 0.456, 0.406], variance=[0.229, 0.224, 0.225]),
])

train_data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    val_processing,
])

if __name__ == '__main__':
    train_dataset = CustomDataset("cats_and_dogs_filtered/train", transform=train_data_augmentation)
    val_dataset = CustomDataset("cats_and_dogs_filtered/validation", transform=val_processing)

    train_loader = CustomDataloader(_dataset=train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = CustomDataloader(_dataset=val_dataset, batch_size=batch_size, shuffle=True)


    # https://keras.io/api/layers/
    model = keras.Sequential()
    model.add(keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3)))
    model.add(layers.Conv2D(16, kernel_size=3, activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(8, 8)))
    model.add(layers.Flatten())
    model.add(layers.Dense(512, activation='relu'))
    model.add(layers.Dense(2, activation='relu'))
    model.summary()

    # https://keras.io/api/optimizers/
    # https://keras.io/api/losses/
    INPUT_OPTIMIZER = tf.keras.optimizers.SGD(learning_rate=lr)
    LOSS = tf.keras.losses.MeanSquaredError(reduction="auto", name="mean_squared_error")
    model.compile(optimizer=INPUT_OPTIMIZER, loss=LOSS)
    model.fit(train_loader, batch_size=batch_size, epochs=n_epochs, validation_data=val_loader)
    model.save("model.keras")

"""
total images:2000
total images:1000
Model: "sequential_2"
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 conv2d (Conv2D)             (None, 148, 148, 16)      448       
                                                                 
 max_pooling2d (MaxPooling2D  (None, 18, 18, 16)       0         
 )                                                               
                                                                 
 flatten (Flatten)           (None, 5184)              0         
                                                                 
 dense (Dense)               (None, 512)               2654720   
                                                                 
 dense_1 (Dense)             (None, 2)                 1026      
                                                                 
=================================================================
Total params: 2,656,194
Trainable params: 2,656,194
Non-trainable params: 0
_________________________________________________________________
Epoch 1/20
100/100 [==============================] - 29s 293ms/step - loss: 0.3131 - val_loss: 0.2775
Epoch 2/20
100/100 [==============================] - 32s 318ms/step - loss: 0.2806 - val_loss: 0.2635
Epoch 3/20
100/100 [==============================] - 61s 607ms/step - loss: 0.2680 - val_loss: 0.2556
Epoch 4/20
100/100 [==============================] - 47s 469ms/step - loss: 0.2581 - val_loss: 0.2543
Epoch 5/20
100/100 [==============================] - 33s 327ms/step - loss: 0.2535 - val_loss: 0.2477
Epoch 6/20
100/100 [==============================] - 32s 324ms/step - loss: 0.2474 - val_loss: 0.2436
Epoch 7/20
100/100 [==============================] - 33s 326ms/step - loss: 0.2450 - val_loss: 0.2413
Epoch 8/20
100/100 [==============================] - 32s 320ms/step - loss: 0.2425 - val_loss: 0.2379
Epoch 9/20
100/100 [==============================] - 32s 319ms/step - loss: 0.2360 - val_loss: 0.2377
Epoch 10/20
100/100 [==============================] - 33s 333ms/step - loss: 0.2353 - val_loss: 0.2386
Epoch 11/20
100/100 [==============================] - 34s 342ms/step - loss: 0.2317 - val_loss: 0.2347
Epoch 12/20
100/100 [==============================] - 32s 320ms/step - loss: 0.2326 - val_loss: 0.2316
Epoch 13/20
100/100 [==============================] - 33s 329ms/step - loss: 0.2298 - val_loss: 0.2310
Epoch 14/20
100/100 [==============================] - 32s 321ms/step - loss: 0.2297 - val_loss: 0.2395
Epoch 15/20
100/100 [==============================] - 32s 320ms/step - loss: 0.2215 - val_loss: 0.2326
Epoch 16/20
100/100 [==============================] - 32s 325ms/step - loss: 0.2241 - val_loss: 0.2275
Epoch 17/20
100/100 [==============================] - 34s 336ms/step - loss: 0.2231 - val_loss: 0.2281
Epoch 18/20
100/100 [==============================] - 32s 323ms/step - loss: 0.2217 - val_loss: 0.2266
Epoch 19/20
100/100 [==============================] - 31s 308ms/step - loss: 0.2207 - val_loss: 0.2265
Epoch 20/20
100/100 [==============================] - 31s 311ms/step - loss: 0.2192 - val_loss: 0.2249
"""