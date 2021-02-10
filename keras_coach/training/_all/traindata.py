# -*- coding: utf-8 -*-

import datetime as dt

import numpy as np
import pandas as pd

from keras_coach.data_handling import get_np_data_sets, get_data_set_spec_for_spy_and_efs


def get_training_data_complete(length_in_days, time_args=None):
    if time_args is None:
        time_args = dict(
            date_start=dt.date(2009, 1, 1),
            date_end=dt.date(2020, 12, 22),
            # time_range=dt.timedelta(days=120),
            )
    data_set_spec = get_data_set_spec_for_spy_and_efs()
    data_set_spec['length_in_days'] = length_in_days
    # data_set_spec['symbols'] = [s for s in data_set_spec['symbols'] if s['name'] == 'ES=F']
    train_data_all = get_np_data_sets(data_set_spec, **time_args)
    return train_data_all


def get_training_data(length_in_days, time_args=None):
    train_data_all = get_training_data_complete(length_in_days, time_args)
    return (train_data_all['np_values'], train_data_all['labels_next'])


def get_training_data_for_multiple_day_lengths(lengths_in_days, time_args=None):
    train_data_dict = dict()
    full_date_df = None
    for len_in_days in lengths_in_days:
        train_data_all = get_training_data_complete(len_in_days, time_args)
        train_data_dict[len_in_days] = train_data_all
        full_date_df = _get_full_date_df_including_validity_col(train_data_all['labels_last'], full_date_df)

    full_date_df.isvalid.replace(np.NaN, False, inplace=True)
    for len_in_days in lengths_in_days:
        train_data_all = train_data_dict[len_in_days]
        ref_index = train_data_all['labels_last'].index
        df_out, np_arr_out = \
            _filter_elements_acc_to_validity_frame(full_date_df, ref_index,
                                                   train_data_all['labels_last'],
                                                   train_data_all['np_values'])
        train_data_all['labels_last'] = df_out
        train_data_all['np_values'] = np_arr_out
        df_out, np_arr_out = \
            _filter_elements_acc_to_validity_frame(full_date_df, ref_index,
                                                   train_data_all['labels_next'])
        train_data_all['labels_next'] = df_out

    ref_df = train_data_dict[lengths_in_days[0]]['labels_last']
    ref_len = len(ref_df)
    for len_in_days in lengths_in_days:
        c_labels_last = train_data_dict[len_in_days]['labels_last']
        assert(len(c_labels_last) == ref_len)
        assert(c_labels_last.index.equals(ref_df.index))
        c_labels_next = train_data_dict[len_in_days]['labels_next']
        assert(len(c_labels_next) == ref_len)
        np_values = train_data_dict[len_in_days]['np_values']
        assert(len(np_values) == ref_len)

    return train_data_dict


def _get_full_date_df_including_validity_col(df_in, full_date_df=None):
    if full_date_df is None:
        full_date_df = pd.DataFrame(index=df_in.index)
        full_date_df = full_date_df.assign(isvalid=True)
    else:
        df_in = df_in.assign(isvalid2=True)
        df_merged = pd.concat([df_in, full_date_df], axis=1)
        df_full_index = pd.DataFrame(index=df_merged.index)
        df_only_valids = df_merged[df_merged.isvalid & df_merged.isvalid2]
        df_only_valids = pd.DataFrame(index=df_only_valids.index)
        df_only_valids = df_only_valids.assign(isvalid2=True)
        full_date_df = pd.concat([df_full_index, full_date_df, df_only_valids], axis=1)
        full_date_df.pop('isvalid')
        full_date_df.rename(columns={"isvalid2": "isvalid"}, inplace=True)
    return full_date_df


def _filter_elements_acc_to_validity_frame(full_date_df, df_ref_index, df_in, np_data=None):
    full_date_df = full_date_df[full_date_df.index.isin(df_ref_index)]
    df_filtered = df_in[full_date_df.isvalid.values]
    if np_data is not None:
        np_bool_hotcoded_filter = full_date_df.isvalid.to_numpy()
        np_data = np_data[np_bool_hotcoded_filter]
    return df_filtered, np_data


def split_data(x_train_data, y_label_data, train_percent=.6, validate_percent=.2,
               hyper_test_percent=.0, seed=None):
    total_len = len(y_label_data)

    # vals = train + validate + test + hyper_val

    # test .. take last values
    test_perc = 1 - train_percent - validate_percent - hyper_test_percent
    hyper_test_len = int(total_len * hyper_test_percent)
    hyper_test_start_id = total_len - hyper_test_len
    x_hyper_test = x_train_data[hyper_test_start_id:]
    y_hyper_test = y_label_data[hyper_test_start_id:]

    test_len = int(total_len * test_perc)
    test_start_id = hyper_test_start_id - test_len
    x_test = x_train_data[test_start_id:]
    y_test = y_label_data[test_start_id:]

    # rest ..split into train and validate
    total_len_rest = total_len - hyper_test_len - test_len
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
                x_test=x_test, y_test=y_test,
                x_hyper_test=x_hyper_test, y_hyper_test=y_hyper_test)
