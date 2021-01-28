
import datetime as dt

import numpy as np
from keras import models
from keras.backend import sigmoid
from keras import utils
from keras import layers

from tensorflow import keras
from tensorflow.keras import layers

from keras_coach.data_handling import get_np_data_sets, get_data_set_spec_for_spy_and_efs

from keras_coach.training import binary_crossentropy
from keras_coach.training._all import swish

# https://github.com/fchollet/deep-learning-with-python-notebooks/blob/master/3.6-classifying-newswires.ipynb


def main():
    swish.register_swish_activation_func()
    x_train_data, y_label_data = _get_training_data()
    _build_model()


def _get_training_data():
    date_end = dt.date(2020, 12, 22)
    time_range = dt.timedelta(days=200)
    data_set_spec = get_data_set_spec_for_spy_and_efs()
    train_data_all = get_np_data_sets(data_set_spec, date_end=date_end, time_range=time_range)

    # Split the data up in train and test sets
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=4)
    x_train_data = train_data_all['np_values']
    y_label_data = binary_crossentropy.extract_labels_from_df(train_data_all['labels'])
    return (x_train_data, y_label_data)


def _build_model():
    model = models.Sequential()
    model.add(layers.Dense(64, activation='swish', input_shape=(10000,)))
    model.add(layers.Dense(64, activation='swish'))
    model.add(layers.Dense(46, activation='softmax'))


def train(x_train_data, y_label_data):
    # Model / data parameters
    num_classes = 10
    input_shape = (28, 28, 1)

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    # Scale images to the [0, 1] range
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    # Make sure images have shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    print("x_train shape:", x_train.shape)
    print(x_train.shape[0], "train samples")
    print(x_test.shape[0], "test samples")

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )

    model.summary()

    batch_size = 128
    epochs = 2

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

    score = model.evaluate(x_test, y_test, verbose=0)
    print("Test loss:", score[0])
    print("Test accuracy:", score[1])


main()
