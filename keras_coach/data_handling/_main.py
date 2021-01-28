# -*- coding: utf-8 -*-

import datetime as dt
import numpy as np

from _misc_frogs.pd_dataframes.resample import downsample_pframe_to_x_minutes
from _write_read import all_in_one

from keras_coach._misc import assert_df
from ._df_operations import time_shift
from ._df_operations.unusable_days import (get_time_vector_containing_not_usable_days,
                                           filter_out_df_batches_with_unusable_days)
from ._df_operations.df_len_adjust import (make_dataframes_min_max_dates_equal,
                                           make_dataframe_days_equally_long)
from ._df_operations.df_batches import (split_data_in_multi_day_batches,
                                        resort_and_summarize_batches_distributed_over_symbols_to_single_batch_for_all_symbols)  # @IgnorePep8

from ._df_operations.normalize import (get_dataframe_with_normalized_training_data_over_complete_range,
                                       get_dataframe_with_normalized_training_data_for_dataset_batches)
from . import _cache

# Denotations
# x = Input-data
# y/labels = Target-value > Value to compare lost-function-output with
# normalize label data

# Train-data > Train with
# Validation-data > Validation to check model after training > Used to check loss-functions-delta
# Test-data > Data used for Hyperparameter training

# shape > (number batches x number data points) x number features
#           > number batches: i.e. one batch is e.g. data for 5 days
#           > number data points: data points in one batch, e.g. 5 days > 5 * 8 * 60 / 5
#                           (8 trading hours, one sample every 5 min)
#           > number features: features are stock price, stock volume, stock ...


def get_data_set_spec_for_spy_and_efs(length_in_days=5):
    data_set_spec = dict(length_in_days=length_in_days,
                         label_symbol='SPY',
                         symbols=[
                             dict(name='SPY',
                                  day_start_time=dt.time(4, 0), day_end_time=dt.time(20, 0),),
                             dict(name='ES=F',
                                  day_start_time=dt.time(18, 0), day_end_time=dt.time(17, 0),
                                  timeshift_adapt_direction="+",)
                         ])
    return data_set_spec


@_cache.get_cached_data_deco
def get_np_data_sets(data_set_spec, date_start=None, date_end=None, time_range=None,
                     sample_period_in_min=5, overlapping=True):
    data_set_length_in_days = data_set_spec['length_in_days']
    symbols_data = list()
    for symb in data_set_spec['symbols']:
        symb_name = symb['name']
        df = all_in_one.get_data_from_date_range_as_dframe(symb_name, date_start, date_end, time_range,
                                                           resample_df=False)
        if 'time' in df.columns:
            df = df.drop('time', axis='columns')
        symbols_data.append(dict(spec=symb, df=df))

    symbols_data = time_shift.shift_symbols_data_time_to_make_days_congruent(symbols_data)

    for symb in symbols_data:
        symb['df'] = downsample_pframe_to_x_minutes(symb['df'], sample_period_in_min)

    symbols_data = make_dataframes_min_max_dates_equal(symbols_data)
    vector_with_not_usable_days = get_time_vector_containing_not_usable_days(symbols_data)

    first_date = None
    for symb in symbols_data:
        symb['df'] = get_dataframe_with_normalized_training_data_over_complete_range(symb['df'])
        first_date = symb['df'].index[0].date() if first_date is None else first_date
        assert(symb['df'].index[0].date() == first_date)
        symb['df'] = make_dataframe_days_equally_long(symb['df'])

        df_batches, vector_with_not_usable_days = \
            split_data_in_multi_day_batches(symb['df'], data_set_length_in_days, vector_with_not_usable_days,
                                            overlapping)
        df_batches = get_dataframe_with_normalized_training_data_for_dataset_batches(df_batches)

        symb.pop('df')
        symb['df_batches'] = df_batches

    batch_len = None
    for symb in symbols_data:
        df_batches = symb['df_batches']
        df_batches = filter_out_df_batches_with_unusable_days(df_batches, vector_with_not_usable_days)
        batch_len = len(df_batches) if batch_len is None else batch_len
        assert(batch_len == len(df_batches))
        df_batches = time_shift.shift_back_symbol_df_batches_time_to_its_original(symb, df_batches)
        assert_df.assert_dfs([db['df'] for db in df_batches])
        symb['df_batches'] = df_batches

    return _convert_to_final_format(data_set_spec, symbols_data)


def _convert_to_final_format(data_set_spec, symbols_data):
    df_batches_per_symb_dict = {symb['spec']['name']: symb['df_batches'] for symb in symbols_data}
    df_per_symb_dict = dict()
    for symb_name in df_batches_per_symb_dict:
        df_batches = df_batches_per_symb_dict[symb_name]
        df_per_symb_dict[symb_name] = [db['df'] for db in df_batches]
    dfs_batch_bin = \
        resort_and_summarize_batches_distributed_over_symbols_to_single_batch_for_all_symbols(df_per_symb_dict)
    assert_df.assert_dfs(dfs_batch_bin)
    label_symbol = data_set_spec['label_symbol']

    df_labels_last_separated = [db['label_last'] for db in df_batches_per_symb_dict[label_symbol]]
    df_labels_last = df_labels_last_separated[0]
    for df_l in df_labels_last_separated[1:]:
        df_labels_last = df_labels_last.append(df_l)
    df_labels_next_separated = [db['label_next'] for db in df_batches_per_symb_dict[label_symbol]]
    df_labels_next = df_labels_next_separated[0]
    for df_l in df_labels_next_separated[1:]:
        df_labels_next = df_labels_next.append(df_l)

    assert(len(dfs_batch_bin) == len(df_labels_last))
    dfs_batch_bin, df_labels_last, df_labels_next = \
        _convert_nan_to_0(dfs_batch_bin, df_labels_last, df_labels_next)
    np_matrix = _convert_to_numpy_multidym_matrix(dfs_batch_bin)

    return dict(np_values=np_matrix, labels_last=df_labels_last, labels_next=df_labels_next)


def _convert_nan_to_0(dfs_batch_bin, df_labels_last, df_labels_next):
    for i_df, df_x in enumerate(dfs_batch_bin):
        dfs_batch_bin[i_df] = df_x.replace(np.NaN, 0)
    assert(len(df_labels_last.loc[df_labels_last.close.isna()]) == 0)
    assert(len(df_labels_last.loc[df_labels_last.open.isna()]) == 0)
    assert(len(df_labels_next.loc[df_labels_next.close.isna()]) == 0)
    assert(len(df_labels_next.loc[df_labels_next.open.isna()]) == 0)
    return dfs_batch_bin, df_labels_last, df_labels_next


def _convert_to_numpy_multidym_matrix(dfs_batch_bin):
    numb_batches = len(dfs_batch_bin)
    numb_data_points = len(dfs_batch_bin[0])
    numb_features = len(dfs_batch_bin[0].columns)
    np_matrix = np.zeros((numb_batches, numb_data_points, numb_features,))
    for i_df, df_x in enumerate(dfs_batch_bin):
        df_x = df_x.replace(np.NaN, 0)
        df_as_np_arr = df_x.to_numpy()
        np_matrix[i_df] = df_as_np_arr
    return np_matrix
