import tensorflow as tf
from data_processing import get_random_sample
import pandas as pd
import numpy as np


batch_size = 15
time_steps = 100
feature_size = 1


def get_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(60, input_shape=(time_steps, feature_size)),
        tf.keras.layers.Dense(20, activation=tf.nn.sigmoid),
        tf.keras.layers.Dense(1)
    ])
    model.summary()
    model.compile(optimizer='adam',
                  loss="mse",
                  metrics=['mae', 'accuracy'],
                  )
    return model


def train(model, data, result):
    batch = tf.reshape(data, [data.shape[0], time_steps, feature_size])
    model.fit(batch, result, epochs=50, batch_size=batch_size, steps_per_epoch=5)


if __name__ == "__main__":
    sample = get_random_sample()
    model = get_model()
    result = tf.convert_to_tensor(pd.DataFrame(np.zeros((sample.shape[0], 1))))
    train(model, sample, result)
