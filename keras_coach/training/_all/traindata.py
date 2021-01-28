# -*- coding: utf-8 -*-

import datetime as dt

import numpy as np
from keras_coach.data_handling import get_np_data_sets, get_data_set_spec_for_spy_and_efs


def get_training_data(length_in_days):
    time_args = dict(
        date_start=dt.date(2009, 1, 1),
        date_end=dt.date(2020, 12, 22),
        # time_range=dt.timedelta(days=120),
        )
    data_set_spec = get_data_set_spec_for_spy_and_efs()
    data_set_spec['length_in_days'] = length_in_days
    # data_set_spec['symbols'] = [s for s in data_set_spec['symbols'] if s['name'] == 'ES=F']
    train_data_all = get_np_data_sets(data_set_spec, **time_args)
    return (train_data_all['np_values'], train_data_all['labels_next'])


def split_data(x_train_data, y_label_data, train_percent=.6, validate_percent=.2, seed=None):
    total_len = len(y_label_data)
    # test .. take last values
    test_perc = 1 - train_percent - validate_percent
    test_len = int(total_len * test_perc)
    x_test = x_train_data[(total_len - test_len):]
    y_test = y_label_data[(total_len - test_len):]

    # rest ..split into train and validate
    total_len_rest = total_len - test_len
    x_train_data = x_train_data[:total_len_rest]
    y_label_data = y_label_data[:total_len_rest]

    np.random.seed(seed)
    # vect_0_to_len = np.array(range(total_len_rest))
    # perm = np.random.permutation(vect_0_to_len)
    train_len = int(total_len * train_percent)
    # perm_train = perm[:train_len]
    # perm_validate = perm[train_len:]

    # x_train = np.take(x_train_data, perm_train, axis=0)
    # y_train = np.take(y_label_data, perm_train, axis=0)
    # x_validate = np.take(x_train_data, perm_validate, axis=0)
    # y_validate = np.take(y_label_data, perm_validate, axis=0)

    x_train = x_train_data[:train_len]
    y_train = y_label_data[:train_len]
    x_validate = x_train_data[train_len:]
    y_validate = y_label_data[train_len:]

    assert(len(x_train) + len(x_validate) + len(x_test) == total_len)
    assert(len(y_train) + len(y_validate) + len(y_test) == total_len)
    assert(len(x_train) == len(y_train))
    assert(len(x_validate) == len(y_validate))
    assert(len(x_test) == len(y_test))
    assert(x_train[0].shape == x_validate[0].shape)
    assert(x_train[0].shape == x_test[0].shape)

    # alternative
    # from sklearn.model_selection import train_test_split
    # x_test, x_validate, y_test, y_validate = \
    #    train_test_split(x_validate, y_validate, test_size=0.5, random_state=4)

    return dict(x_train=x_train, y_train=y_train,
                x_validate=x_validate, y_validate=y_validate,
                x_test=x_test, y_test=y_test)
