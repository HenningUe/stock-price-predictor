
import random

from keras import models, layers, optimizers, metrics, regularizers  # @UnusedImport

from keras_coach.training._all import debug, traindata
from keras_coach.training.scalar_regression._common import extract_np_labels_from_df_raw
from ._callbacks import EarlyStoppingCustom


def objective_func(x_train_data, y_label_df_raw, params):
    build_mdl_funcname = params['funcname']
    if build_mdl_funcname == 'dense_pure':
        build_model_func = _build_model_dense_pure
    elif build_mdl_funcname == 'cnn_pure':
        build_model_func = _build_model_cnn_pure
    elif build_mdl_funcname == 'rnn_lstm_pure':
        build_model_func = _build_model_rnn_lstm_pure
    elif build_mdl_funcname == 'rnn_lstm_with_cnn':
        build_model_func = _build_model_rnn_lstm_with_cnn

    y_label_data = extract_np_labels_from_df_raw(y_label_df_raw)
    # Split the data up in train and test sets
    data = traindata.split_data(x_train_data, y_label_data)

    model = build_model_func(data['x_train'], params)
    save_mdl_params = None
    if debug.HYPEROPT_SIMULATE:
        acc = -random.random()
    else:
        callb = EarlyStoppingCustom(dict(x=data['x_validate'], y=data['y_validate']))
        MAX_EPOCHS = 100
        model.fit(data['x_train'], data['y_train'],
                  epochs=MAX_EPOCHS,
                  validation_data=(data['x_validate'], data['y_validate']),
                  callbacks=[callb])

        if callb.best_guess is not None:
            save_mdl_params = dict(epoch=callb.best_guess['epoch'],
                                   reference_value=float(callb.best_guess['precision_total']))
        acc = -float(callb.best_guess['precision_total'])
    return dict(acc=acc, model=model, save_mdl_params=save_mdl_params)


def _build_model_dense_pure(x_train_data, params):
    from keras_coach.training._all.models_hyperopt import space_and_mdl_templates
    model = space_and_mdl_templates.build_model_dense_pure(x_train_data, params)
    return _finish_and_compile_mdl(model)


def _build_model_rnn_lstm_pure(x_train_data, params):
    from keras_coach.training._all.models_hyperopt import space_and_mdl_templates
    model = space_and_mdl_templates.build_model_rnn_lstm_pure(x_train_data, params)
    return _finish_and_compile_mdl(model)


def _build_model_cnn_pure(x_train_data, params):
    from keras_coach.training._all.models_hyperopt import space_and_mdl_templates
    model = space_and_mdl_templates.build_model_cnn_pure(x_train_data, params)
    return _finish_and_compile_mdl(model)


def _build_model_rnn_lstm_with_cnn(x_train_data, params):
    from keras_coach.training._all.models_hyperopt import space_and_mdl_templates
    model = space_and_mdl_templates.build_model_rnn_lstm_with_cnn(x_train_data, params)
    return _finish_and_compile_mdl(model)


def _finish_and_compile_mdl(model):
    model.add(layers.Dense(1))
    if debug.HYPEROPT_SIMULATE:
        model = None
    else:
        opt = optimizers.RMSprop(lr=0.001)
        model.compile(optimizer=opt, loss='mse', metrics=['mae'])
    return model