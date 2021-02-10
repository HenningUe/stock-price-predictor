# -*- coding: utf-8 -*-

import datetime as dt
import numpy as np

from keras_coach.training._all import swish, model_store, traindata, hyperopt_store


def predict(x_data_in=None):

    swish.register_swish_activation_func()
    mode = 1
    if mode == 0:
        model_ids = hyperopt_store.load_hyper_hyperopt_models()
        mdl_bins = model_store.get_models(model_ids=model_ids)
    elif mode == 1:
        mdl_bins = list()
        funcs = ['dense_pure', 'cnn_pure', 'rnn_lstm_pure', 'rnn_lstm_with_cnn']
        funcs = ['cnn_pure', 'rnn_lstm_pure']
        for f in funcs:
            mdl_binsx = model_store.get_models_sorted_by_reference_value(f)
            for i in range(2):
                mdl_bins.append(mdl_binsx[i])
    vector_positive_predicts_1 = None
    for mdl_bin in mdl_bins:
        model = mdl_bin.load_model()
        x_data = x_data_in
        if callable(x_data):
            x_data = x_data(mdl_bin.length_in_days)
        test_predict = model.predict(x_data)
        test_predict = test_predict.reshape(test_predict.shape[0] * test_predict.shape[1])
        vector_positive_predicts = test_predict >= 0
        if vector_positive_predicts_1 is not None:
            # dstack = zip
            comb = np.dstack((vector_positive_predicts, vector_positive_predicts_1,))
            comb = comb[0]
            vector_positive_predicts_1 = np.array([_get_n(xi) for xi in comb])
        else:
            vector_positive_predicts_1 = vector_positive_predicts
    return vector_positive_predicts_1


def _get_n(x):
    val = x[0] if x[0] == x[1] else np.NaN
    return val


def _hyper_hyper_validate():
    TIME_ARGS = dict(date_start=dt.date(2019, 1, 20),
                     date_end=dt.date(2020, 12, 22),)
    DAYS_TO_GET = [1, 2, 3, 4, 5, 6, 7]
    train_data_dict = traindata.get_training_data_for_multiple_day_lengths(DAYS_TO_GET, time_args=TIME_ARGS)

    def extract(len_in_days):
        train_data = train_data_dict[len_in_days]
        x_train_data = train_data['np_values']
        return x_train_data

    from keras_coach.training import scalar_regression
    # x_train_data, y_label_df_raw = traindata.get_training_data(len_in_days)

    rtn_val = predict(extract)

    train_data = train_data_dict[2]
    y_label_df_raw = train_data['labels_next']
    y_label_data = scalar_regression.extract_np_labels_from_df_raw(y_label_df_raw)
    y_label_data = y_label_data >= 0
    total_true = 0
    correct_true = 0
    total_false = 0
    correct_false = 0
    for i in range(len(rtn_val)):
        pv = rtn_val[i]
        if pv == np.NaN:
            continue
        is_v = y_label_data[i]
        if pv == 1:
            total_true += 1
            if is_v:
                correct_true += 1
        if pv == 0:
            total_false += 1
            if not is_v:
                correct_false += 1
    print(total_true)
    print(correct_true)
    print(total_false)
    print(correct_false)


if __name__ == "__main__":

    _hyper_hyper_validate()
