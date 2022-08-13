import numpy as np
import tensorflow as tf
import math
import matplotlib.pyplot as plt


if __name__ == '__main__':
    flag = False
    fig, ax = plt.subplots()
    for model_name in ["model_rnn.keras", "model_lstm.keras", "model_nn.keras"]:
        model = tf.keras.models.load_model(model_name)
        model.summary()
        timed_y_list = []
        graph_data = []
        x_list = []
        time_step_size = 5
        predict_count = 20
        for xx in range(14400, 14400+predict_count+time_step_size, 1):
            x = xx / 1000.0
            y = 2.0 * math.sin(x) + math.sin(2.0 * x) + math.sin(6.0 * x) + math.cos(x) + 4.0
            timed_y_list.append(y)

        timed_y_data = np.array(timed_y_list)

        x_list.extend(timed_y_list[0:time_step_size])
        graph_data.extend(timed_y_list[0:time_step_size])
        for idx in range(predict_count):
            print("xlist",x_list)
            x_data = np.array(x_list)
            if model_name == "model_nn.keras":
                rsdata = np.reshape(x_data, (1, 5))
                print(rsdata)
                y = model.predict(rsdata, batch_size=1)
            else:
                rsdata = np.reshape(x_data, (1, -1, 1))
                print(rsdata)
                y = model.predict(rsdata, batch_size=1)
            print("y", y)
            x_list.append(y[0][0])
            x_list.pop(0)
            graph_data.append(y[0][0])

        if not flag:
            flag = True
            ax.plot(timed_y_data, label="real")

        ax.plot(np.array(graph_data), label=model_name)

    plt.legend()
    plt.savefig("tester.png")