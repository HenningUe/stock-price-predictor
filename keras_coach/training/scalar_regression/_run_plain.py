
from keras import models, layers, optimizers, metrics  # @UnusedImport
from ._mdl_compile import finish_and_compile_mdl


def build_model_recurrent_lstm(x_train_data):
    model = models.Sequential()
    model.add(layers.recurrent.LSTM(200, return_sequences=True,
                                    input_shape=(x_train_data.shape[1], x_train_data.shape[2])))
    model.add(layers.recurrent.LSTM(200, return_sequences=False))
    model.add(layers.Dense(80, activation='swish'))
    model = finish_and_compile_mdl(model)
    return model


def build_model_recurrent_lstm_with_cnn(x_train_data):
    # inputs = models.Input(batch_shape=(x_train_data[0], 1, x_train_data[1] + 1))

    model = models.Sequential()
    model.add(layers.Conv1D(80, (8), activation='swish', input_shape=(x_train_data.shape[1], x_train_data.shape[2],)))
    model.add(layers.MaxPooling1D(8))
    # model.add(layers.Conv1D(200, (12), activation='swish'))
    model.add(layers.normalization.BatchNormalization())
    # model.add(layers.recurrent.LSTM(130, dropout=0.1, return_sequences=True))
    model.add(layers.recurrent.LSTM(80, dropout=0.1, return_sequences=False))
    model.add(layers.normalization.BatchNormalization())
    model.add(layers.Dense(60, activation='swish'))
    model.add(layers.Dense(1))
    model = finish_and_compile_mdl(model)


def build_model_dense_pure(x_train_data):
    # Because we will need to instantiate
    # the same model multiple times,
    # we use a function to construct it.
    model = models.Sequential()
    model.add(layers.Dense(250, activation='swish',
                           input_shape=(x_train_data.shape[1], x_train_data.shape[2],)))
    model.add(layers.Dropout(0.3))
    model.add(layers.Dense(250, activation='swish'))
#     model.add(layers.Dropout(0.3))
#     model.add(layers.Dense(128, activation='swish'))
#     model.add(layers.Dropout(0.3))
#     model.add(layers.Dense(128, activation='tanh'))
    model.add(layers.Flatten())
    model = finish_and_compile_mdl(model)


def build_model_cnn(x_train_data):
    model = models.Sequential()
    model.add(layers.normalization.BatchNormalization())
    model.add(layers.Conv1D(50, (12), activation='swish', input_shape=(x_train_data.shape[1], x_train_data.shape[2],)))
    model.add(layers.AveragePooling1D((10)))
    model.add(layers.Conv1D(80, (12), activation='swish'))
    # model.add(layers.AveragePooling1D((10)))
#     model.add(layers.MaxPooling1D((2)))
#     model.add(layers.Conv1D(64, (3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(300, activation='swish'))
    model = finish_and_compile_mdl(model)


class BuildMdlFuncs:
    build_model_dense_pure = build_model_dense_pure
    build_model_recurrent_lstm = build_model_recurrent_lstm
    build_model_cnn = build_model_cnn
    build_model_recurrent_lstm_with_cnn = build_model_recurrent_lstm_with_cnn
