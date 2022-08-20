import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pickle
from tensorflow.keras.utils import to_categorical


if __name__ == '__main__':

    with open('char_to_index.pickle', 'rb') as fr:
        char_to_index = pickle.load(fr)

    with open('index_to_char.pickle', 'rb') as fr:
        index_to_char = pickle.load(fr)

    flag = False
    fig, ax = plt.subplots()
    for model_name in ["model_lstm.keras"]:
        model = tf.keras.models.load_model(model_name)
        model.summary()
        x_list = []
        x_list.extend(" 삼천리")
        predict_count = 30

        for idx in range(predict_count):
            print("xlist",x_list)
            x_data = np.array([[to_categorical(char_to_index[i], 85) for i in x_list]])
            print(x_data.shape)
            y = model.predict(x_data, batch_size=1)
            #print("y:", y)
            result = np.argmax(y, axis=1)
            print("result:", result)
            newchar = index_to_char[int(result)]
            print("newchar:", newchar)
            x_list.append(newchar)
            x_list.pop(0)

'''
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
xlist [' ', '삼', '천', '리']
(1, 4, 85)
1/1 [==============================] - 0s 275ms/step
result: [0]
newchar:  
xlist ['삼', '천', '리', ' ']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [83]
newchar: 화
xlist ['천', '리', ' ', '화']
(1, 4, 85)
1/1 [==============================] - 0s 10ms/step
result: [34]
newchar: 려
xlist ['리', ' ', '화', '려']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [0]
newchar:  
xlist [' ', '화', '려', ' ']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [5]
newchar: 강
xlist ['화', '려', ' ', '강']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [53]
newchar: 산
xlist ['려', ' ', '강', '산']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [25]
newchar: 대
xlist [' ', '강', '산', '대']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [80]
newchar: 한
xlist ['강', '산', '대', '한']
(1, 4, 85)
1/1 [==============================] - 0s 11ms/step
result: [0]
newchar:  
xlist ['산', '대', '한', ' ']
(1, 4, 85)
1/1 [==============================] - 0s 10ms/step
result: [52]
newchar: 사
xlist ['대', '한', ' ', '사']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [32]
newchar: 람
xlist ['한', ' ', '사', '람']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [1]
newchar: ,
xlist [' ', '사', '람', ',']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [0]
newchar:  
xlist ['사', '람', ',', ' ']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [25]
newchar: 대
xlist ['람', ',', ' ', '대']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [80]
newchar: 한
xlist [',', ' ', '대', '한']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [67]
newchar: 으
xlist [' ', '대', '한', '으']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [35]
newchar: 로
xlist ['대', '한', '으', '로']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [0]
newchar:  
xlist ['한', '으', '로', ' ']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [14]
newchar: 길
xlist ['으', '로', ' ', '길']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [57]
newchar: 성
xlist ['로', ' ', '길', '성']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [0]
newchar:  
xlist [' ', '길', '성', ' ']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [50]
newchar: 보
xlist ['길', '성', ' ', '보']
(1, 4, 85)
1/1 [==============================] - 0s 13ms/step
result: [73]
newchar: 전
xlist ['성', ' ', '보', '전']
(1, 4, 85)
1/1 [==============================] - 0s 9ms/step
result: [0]
newchar:  
xlist [' ', '보', '전', ' ']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [58]
newchar: 세
xlist ['보', '전', ' ', '세']
(1, 4, 85)
1/1 [==============================] - 0s 12ms/step
result: [2]
newchar: .
xlist ['전', ' ', '세', '.']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [3]
newchar: 가
xlist [' ', '세', '.', '가']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [44]
newchar: 무
xlist ['세', '.', '가', '무']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [0]
newchar:  
xlist ['.', '가', '무', ' ']
(1, 4, 85)
1/1 [==============================] - 0s 8ms/step
result: [79]
newchar: 하
'''