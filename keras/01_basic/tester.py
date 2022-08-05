import numpy as np
import tensorflow as tf

if __name__ == '__main__':
    model = tf.keras.models.load_model("model.keras")
    model.summary()

    # test
    x_prd = np.array([[0.1, 0.2, 0.1]])  # y = 1 + 2*0.1*0.2*0.1
    print("expect:", 1 + 2 * 0.1 * 0.2 * 0.1)
    print(model.predict(x_prd))
