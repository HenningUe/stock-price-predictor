# -*- coding: utf-8 -*-

from keras import models, layers, metrics, optimizers, losses, regularizers, activations  # @UnusedImport
from ._mdl_compile import finish_and_compile_mdl


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
    model = finish_and_compile_mdl(model)
    return model


def build_model_cnn(x_train_data):
    model = models.Sequential()
    model.add(layers.Conv1D(32, (3), activation='relu', input_shape=(x_train_data.shape[1], x_train_data.shape[2],)))
    model.add(layers.MaxPooling1D((2)))
    model.add(layers.Conv1D(64, (3), activation='relu'))
    model.add(layers.Flatten())
    # model.add(layers.Dropout(0.1))
    model.add(layers.Dense(64, activation='relu'))
    model = finish_and_compile_mdl(model)
    return model


class BuildMdlFuncs:
    build_model_dense_pure = build_model_dense_pure
    build_model_cnn = build_model_cnn
