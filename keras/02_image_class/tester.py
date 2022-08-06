import numpy as np
import tensorflow as tf
from PIL import Image
import trainer


if __name__ == '__main__':
    model = tf.keras.models.load_model("model.keras")
    model.summary()

    train_dataset = trainer.CustomDataset("cats_and_dogs_filtered/train", transform=trainer.val_processing)
    val_dataset = trainer.CustomDataset("cats_and_dogs_filtered/validation", transform=trainer.val_processing)

    train_loader = trainer.CustomDataloader(_dataset=train_dataset, batch_size=1, shuffle=True)
    val_loader = trainer.CustomDataloader(_dataset=val_dataset, batch_size=1, shuffle=True)

    # test
    test_images = ["cats_and_dogs_filtered/train/cats/cat.1.jpg",
                   "cats_and_dogs_filtered/train/cats/cat.2.jpg",
                   "cats_and_dogs_filtered/train/dogs/dog.1.jpg",
                   "cats_and_dogs_filtered/train/dogs/dog.2.jpg",
                   "cats_and_dogs_filtered/validation/cats/cat.2001.jpg",
                   "cats_and_dogs_filtered/validation/dogs/dog.2001.jpg",
                   "cats_and_dogs_filtered/validation/cats/cat.2004.jpg",
                   "cats_and_dogs_filtered/validation/dogs/dog.2004.jpg",
                   ]

    for test_image in test_images:
        print(test_image)
        dataset = trainer.CustomDataset("cats_and_dogs_filtered/train", transform=trainer.val_processing, file_name=test_image)
        dataloader = trainer.CustomDataloader(_dataset=dataset, batch_size=1, shuffle=False)
        x_prd = dataloader[0][0]  # batch 0 , x
        print(x_prd.shape)
        y = model.predict(x_prd)
        print("result:", y)
        if y[0][0] > y[0][1]:
            print("cat")
        else:
            print("dog")

"""
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
total images:2000
total images:1000
cats_and_dogs_filtered/train/cats/cat.1.jpg
(1, 150, 150, 3)
1/1 [==============================] - 0s 60ms/step
result: [[0.48046866 0.43707907]]
cat
cats_and_dogs_filtered/train/cats/cat.2.jpg
(1, 150, 150, 3)
1/1 [==============================] - 0s 12ms/step
result: [[0.74900883 0.4924001 ]]
cat
cats_and_dogs_filtered/train/dogs/dog.1.jpg
(1, 150, 150, 3)
1/1 [==============================] - 0s 12ms/step
result: [[0.45707452 0.7523619 ]]
dog
cats_and_dogs_filtered/train/dogs/dog.2.jpg
(1, 150, 150, 3)
1/1 [==============================] - 0s 12ms/step
result: [[0.15739511 0.7101962 ]]
dog
cats_and_dogs_filtered/validation/cats/cat.2001.jpg
(1, 150, 150, 3)
1/1 [==============================] - 0s 10ms/step
result: [[0.63321704 0.2585028 ]]
cat
cats_and_dogs_filtered/validation/dogs/dog.2001.jpg
(1, 150, 150, 3)
1/1 [==============================] - 0s 12ms/step
result: [[0.1274486  0.65480846]]
dog
cats_and_dogs_filtered/validation/cats/cat.2004.jpg
(1, 150, 150, 3)
1/1 [==============================] - 0s 11ms/step
result: [[0.73557734 0.3226891 ]]
cat
cats_and_dogs_filtered/validation/dogs/dog.2004.jpg
(1, 150, 150, 3)
1/1 [==============================] - 0s 12ms/step
result: [[0.48342577 0.7902105 ]]
dog
"""