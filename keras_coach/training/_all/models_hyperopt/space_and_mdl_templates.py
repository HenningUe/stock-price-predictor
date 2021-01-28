
from keras import models, layers, optimizers, metrics, regularizers  # @UnusedImport
import hyperopt as hypopt

choice = hypopt.hp.choice
uniform = hypopt.hp.uniform
uniformint = hypopt.hp.uniformint

SPACE_DENSE_PURE = \
    dict(funcname='dense_pure',
         units1_1_1=uniformint('units1_1_1', 16, 260),
         dropout1_1_2=uniform('dropout1_1_2', .05, .5),
         units1_1_2=uniformint('units1_1_2', 16, 260),
         regular1_1_2=uniform('regular1_1_2', 0, .01),
         layers=choice('num_dense_layers1_1', [dict(num_dense_layers1_1=2),
                                               dict(num_dense_layers1_1=3,
                                                    dropout1_1_3=uniform('dropout1_1_3', .05, .5),
                                                    units1_1_3=uniformint('units1_1_3', 16, 260),
                                                    regular1_1_3=uniform('regular1_1_3', 0, .01),
                                                    )
                                               ]
                       ),
         )

SPACE_RNN_LSTM_PURE = \
    dict(funcname='rnn_lstm_pure',
         units2_1_1=uniformint('units2_1_1', 40, 260),
         recurrent_dropout2_1_1=uniform('recurrent_dropout2_1_1', .05, .5),
         layers=choice('num_lstm_layers2_1', [dict(num_lstm_layers2_1=1),
                                              dict(num_lstm_layers2_1=2,
                                                   recurrent_dropout2_1_2=uniform('recurrent_dropout2_1_2', .05, .5),
                                                   units2_1_2=uniformint('units2_1_2', 40, 260),)
                                              ]
                       ),
         units2_1_3=uniformint('units2_1_3', 16, 120),
         regular2_1_3=uniform('regular2_1_3', 0, .01),
         )

SPACE_CNN_PURE = \
    dict(funcname='cnn_pure',
         units3_1_1=uniformint('units3_1_1', 20, 160),
         kernel3_1_1=uniformint('kernel3_1_1', 4, 12),
         maxpool3_1_1=uniformint('maxpool3_1_1', 4, 12),
         dropout3_1_1=uniform('dropout3_1_1', .05, .3),
         layers=choice('num_cnn_layers3_1', [dict(num_cnn_layers3_1=1),
                                             dict(num_cnn_layers3_1=2,
                                                  units3_1_2=uniformint('units3_1_2', 20, 160),
                                                  kernel3_1_2=uniformint('kernel3_1_2', 4, 12),
                                                  maxpool3_1_2=uniformint('maxpool3_1_2', 4, 12),),
                                             dict(num_cnn_layers3_1=3,
                                                  units3_1_3_1=uniformint('units3_1_3_1', 20, 160),
                                                  kernel3_1_3_1=uniformint('kernel3_1_3_1', 4, 12),
                                                  maxpool3_1_3_1=uniformint('maxpool3_1_3_1', 4, 12),
                                                  units3_1_3_2=uniformint('units3_1_3_2', 20, 160),
                                                  kernel3_1_3_2=uniformint('kernel3_1_3_2', 4, 12),
                                                  maxpool3_1_3_2=uniformint('maxpool3_1_3_2', 4, 12),),
                                             ]
                       ),
         dropout3_1_3=uniform('dropout3_1_3', .05, .3),
         units3_1_4=uniformint('units3_1_4', 16, 200),
         regular3_1_4=uniform('regular3_1_4', 0, .01),
         )

SPACE_RNN_LSTM_WITH_CNN = \
    dict(funcname='rnn_lstm_with_cnn',
         units4_1_1=uniformint('units4_1_1', 20, 160),
         kernel4_1_1=uniformint('kernel4_1_1', 4, 12),
         maxpool4_1_1=uniformint('maxpool4_1_1', 4, 12),
         layers_cnn=choice('num_cnn_layers4_1', [dict(num_cnn_layers4_1=1),
                                                 dict(num_cnn_layers4_1=2,
                                                      units4_1_2=uniformint('units4_1_2', 20, 160),
                                                      kernel4_1_2=uniformint('kernel4_1_2', 4, 12),
                                                      maxpool4_1_2=uniformint('maxpool4_1_2', 4, 12),),
                                                 ]),
         units4_2_1=uniformint('units4_2_1', 40, 260),
         recurrent_dropout4_2_1=uniform('recurrent_dropout4_2_1', .05, .5),
         layers_lstm=choice('num_lstm_layers4_2', [dict(num_lstm_layers4_2=1),
                                                   dict(num_lstm_layers4_2=2,
                                                        recurrent_dropout4_2_2=uniform('recurrent_dropout4_2_2', .05, .5),  # @IgnorePep8
                                                        units4_2_2=uniformint('units4_2_2', 40, 260),)
                                                   ]),
         units4_3_3=uniformint('units4_3_3', 40, 260),
         regular4_3_3=uniform('regular4_3_3', 0, .01),
         )

SPACE_DATA_DAY_LEN = uniformint('num_days', 1, 7)

SPACE_COMBINED = dict(data_day_len=SPACE_DATA_DAY_LEN,
                      mdlfuncs=choice('mdlfunc', [SPACE_DENSE_PURE, SPACE_CNN_PURE,
                                                  SPACE_RNN_LSTM_PURE, SPACE_RNN_LSTM_WITH_CNN],)
                      )


def get_hyperopt_space(get_functions_individual=False):
    global SPACE_COMBINED, SPACE_DATA_DAY_LEN, SPACE_DENSE_PURE, SPACE_RNN_LSTM_PURE, SPACE_RNN_LSTM_WITH_CNN
    if not get_functions_individual:
        return [SPACE_COMBINED]
    else:
        items = [SPACE_DENSE_PURE, SPACE_RNN_LSTM_PURE, SPACE_CNN_PURE, SPACE_RNN_LSTM_WITH_CNN]
        for it in items:
            it.update(dict(data_day_len=SPACE_DATA_DAY_LEN,))
        return items


def build_model_dense_pure(x_train_data, params):
    model = models.Sequential()
    model.add(layers.Dense(params['units1_1_1'], activation='swish',
                           input_shape=(x_train_data.shape[1], x_train_data.shape[2],)))
    model.add(layers.Dropout(params['dropout1_1_2']))
    model.add(layers.Dense(params['units1_1_2'], activation='swish',
                           kernel_regularizer=regularizers.l1(params['regular1_1_2'])))
    if params['layers']['num_dense_layers1_1'] >= 3:
        model.add(layers.Dropout(params['layers']['dropout1_1_3']))
        model.add(layers.Dense(params['layers']['units1_1_3'], activation='swish',
                               kernel_regularizer=regularizers.l1(params['layers']['regular1_1_3'])))
    model.add(layers.Flatten())
    return model


def build_model_rnn_lstm_pure(x_train_data, params):
    model = models.Sequential()
    return_sequences = params['layers']['num_lstm_layers2_1'] > 1
    model.add(layers.recurrent.LSTM(params['units2_1_1'], return_sequences=return_sequences,
                                    recurrent_dropout=params['recurrent_dropout2_1_1'],
                                    input_shape=(x_train_data.shape[1], x_train_data.shape[2])))
    if params['layers']['num_lstm_layers2_1'] >= 2:
        model.add(layers.recurrent.LSTM(params['layers']['units2_1_2'], return_sequences=False,
                                        recurrent_dropout=params['layers']['recurrent_dropout2_1_2'],))
    model.add(layers.Dense(params['units2_1_3'], activation='swish',
                           kernel_regularizer=regularizers.l1(params['regular2_1_3'])))
    model.add(layers.Flatten())
    return model


def build_model_cnn_pure(x_train_data, params):
    model = models.Sequential()
    model.add(layers.normalization.BatchNormalization())
    model.add(layers.Conv1D(params['units3_1_1'], params['kernel3_1_1'], activation='swish',
                            input_shape=(x_train_data.shape[1], x_train_data.shape[2],)))
    model.add(layers.MaxPooling1D(params['maxpool3_1_1']))
    model.add(layers.Dropout(params['dropout3_1_1']))
    if params['layers']['num_cnn_layers3_1'] == 2:
        model.add(layers.Conv1D(params['layers']['units3_1_2'],
                                params['layers']['kernel3_1_2'], activation='swish'))
        model.add(layers.MaxPooling1D(params['layers']['maxpool3_1_2']))
    elif params['layers']['num_cnn_layers3_1'] == 3:
        model.add(layers.Conv1D(params['layers']['units3_1_3_1'],
                                params['layers']['kernel3_1_3_1'], activation='swish'))
        model.add(layers.MaxPooling1D(params['layers']['maxpool3_1_3_1']))
        model.add(layers.Conv1D(params['layers']['units3_1_3_2'],
                                params['layers']['kernel3_1_3_2'], activation='swish'))
        model.add(layers.MaxPooling1D(params['layers']['maxpool3_1_3_2']))
    model.add(layers.Dropout(params['dropout3_1_3']))
    model.add(layers.Flatten())
    model.add(layers.Dense(params['units3_1_4'], activation='swish',
                           kernel_regularizer=regularizers.l1(params['regular3_1_4'])))
    model.add(layers.Flatten())
    return model


def build_model_rnn_lstm_with_cnn(x_train_data, params):
    model = models.Sequential()
    model.add(layers.Conv1D(params['units4_1_1'], params['kernel4_1_1'], activation='swish',
                            input_shape=(x_train_data.shape[1], x_train_data.shape[2],)))
    model.add(layers.MaxPooling1D(params['maxpool4_1_1']))
    if params['layers_cnn']['num_cnn_layers4_1'] == 2:
        model.add(layers.Conv1D(params['layers_cnn']['units4_1_2'],
                                params['layers_cnn']['kernel4_1_2'], activation='swish'))
        model.add(layers.MaxPooling1D(params['layers_cnn']['maxpool4_1_2']))
    return_sequences = params['layers_lstm']['num_lstm_layers4_2'] > 1
    model.add(layers.recurrent.LSTM(params['units4_2_1'], return_sequences=return_sequences,
                                    recurrent_dropout=params['recurrent_dropout4_2_1']))
    if params['layers_lstm']['num_lstm_layers4_2'] >= 2:
        model.add(layers.recurrent.LSTM(params['layers_lstm']['units4_2_2'], return_sequences=False,
                                        recurrent_dropout=params['layers_lstm']['recurrent_dropout4_2_2'],))
    model.add(layers.Dense(params['units4_3_3'], activation='swish',
                           kernel_regularizer=regularizers.l1(params['regular4_3_3'])))
    model.add(layers.Flatten())
    return model
