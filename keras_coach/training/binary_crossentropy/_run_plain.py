# -*- coding: utf-8 -*-

from keras import models, layers, metrics, optimizers, losses, regularizers, activations  # @UnusedImport


def build_model_dense_pure(x_train_data):
    model = models.Sequential()
    model.add(layers.Dense(20, activation='swish', input_shape=(x_train_data.shape[1], x_train_data.shape[2],)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(20, activation='swish', kernel_regularizer=regularizers.l1(0.005)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(20, activation='swish', kernel_regularizer=regularizers.l1(0.005)))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(20, activation='swish', kernel_regularizer=regularizers.l1(0.005)))
    model.add(layers.Flatten())
    model.add(layers.Dense(1, activation='sigmoid'))
    # opt = optimizers.SGD(lr=0.0005)
    opt = optimizers.RMSprop(lr=0.001)
    model.compile(optimizer=opt,
                  loss=losses.binary_crossentropy,
                  metrics=['accuracy'])
    return model


def build_model_cnn(x_train_data):
    model = models.Sequential()
    model.add(layers.Conv1D(32, (3), activation='relu', input_shape=(x_train_data.shape[1], x_train_data.shape[2],)))
    model.add(layers.MaxPooling1D((2)))
    model.add(layers.Conv1D(64, (3), activation='relu'))
    model.add(layers.Flatten())
    # model.add(layers.Dropout(0.1))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))
    # opt = optimizers.SGD(lr=0.002)
    opt = optimizers.RMSprop(lr=0.001)
    model.compile(optimizer=opt,
                  loss=losses.binary_crossentropy,
                  metrics=['accuracy'])
    return model


class BuildMdlFuncs:
    build_model_dense_pure = build_model_dense_pure
    build_model_cnn = build_model_cnn
