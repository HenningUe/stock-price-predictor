
import datetime as dt
from collections import defaultdict

import numpy as np
import pandas as pd
from pandas.tseries.offsets import BusinessDay

from .analysing import get_min_and_max_day_time_of_multiple_dfs


def split_data_in_multi_day_batches(df, data_set_length_in_days, vector_with_not_usable_days, overlapping=True):
    c_date = df.index[0].date()
    last_date = df.index[-1].date()
    df_splitted = list()
    while True:
        new_end_date = (c_date + BusinessDay(data_set_length_in_days - 1)).date()
        if new_end_date > last_date:
            break
        df_label_last = df.loc[(df.index.date == new_end_date)]
        label_next_date = (new_end_date + BusinessDay(1)).date()
        df_label_next = df.loc[(df.index.date == label_next_date)]
        dx = df.loc[(df.index.date >= c_date) & (df.index.date <= new_end_date)]
        dx_dates = np.unique(dx.index.date)
        if len(dx_dates) == 0 \
           or len(dx_dates) < data_set_length_in_days or len(df_label_next) == 0:
            vector_with_not_usable_days = np.append(vector_with_not_usable_days, c_date)
        else:
            open_val_last = df_label_last.loc[df_label_last.open.first_valid_index()].open
            close_val_last = df_label_last.loc[df_label_last.close.last_valid_index()].close
            label_last_data = dict(open=[open_val_last], close=[close_val_last])
            df_label_last = pd.DataFrame(label_last_data, columns=['open', 'close'],
                                         index=pd.DatetimeIndex([df_label_last.index.date[0]]))

            open_val_next = df_label_next.loc[df_label_next.open.first_valid_index()].open
            close_val_next = df_label_next.loc[df_label_next.close.last_valid_index()].close
            label_next_data = dict(open=[open_val_next], close=[close_val_next])
            df_label_next = pd.DataFrame(label_next_data, columns=['open', 'close'],
                                         index=pd.DatetimeIndex([df_label_next.index.date[0]]))
            df_splitted.append(dict(df=dx, label_last=df_label_last, label_next=df_label_next))
        if overlapping:
            c_date = (c_date + BusinessDay(1)).date()
        else:
            c_date = (new_end_date + BusinessDay(1)).date()
    return df_splitted, vector_with_not_usable_days


def filter_out_df_batches_with_unusable_days(df_batches, vector_with_not_usable_days):
    df_with_not_usable_days = pd.DataFrame(vector_with_not_usable_days, columns=list(['date', ]))
    df_with_not_usable_days.index = pd.RangeIndex(0, len(df_with_not_usable_days))
    _get_date = lambda series_in: series_in.index[0].date()  # @IgnorePep8
    filtered_dfs = list()
    for df in df_batches:
        df_group = df.groupby([df.index.year, df.index.month, df.index.day]).agg({'date': _get_date})
        df_group.index = pd.RangeIndex(0, len(df_group))
        df_group_not_usable_days = pd.merge(df_group, df_with_not_usable_days, on='date', how='inner')
        if df_group_not_usable_days.empty:
            filtered_dfs.append(df)
    return filtered_dfs


def resort_and_summarize_batches_distributed_over_symbols_to_single_batch_for_all_symbols(df_batches_per_symb):
    # umsortieren, d.h. batches, die verschiedenen symb zugeordnet sind, sollen zeitl. zueinander
    # angeordnet werden
    batch_count = None
    dfs_batch_bin = defaultdict(list)
    for symb in df_batches_per_symb:
        df_batched = df_batches_per_symb[symb]
        batch_count = len(df_batched) if batch_count is None else batch_count
        assert(len(df_batched) == batch_count)
        for i, batch in enumerate(df_batched):
            dfs_batch_bin[i].append(batch)

    # einzel-batches zusammenfassen
    dfs_batch_bin_rtn = list()
    len_df_batch_bin = None
    for k in sorted(dfs_batch_bin.keys()):
        batched_dfs = dfs_batch_bin[k]
        df_merged = batched_dfs[0]
        for i, df in enumerate(batched_dfs[1:]):
            df_merged = df_merged.join(df, rsuffix=f"_{i}", how="outer")
        len_df_batch_bin = len(df_merged) if len_df_batch_bin is None else len_df_batch_bin
        dfs_batch_bin_rtn.append(df_merged)

    dfs_batch_bin_rtn = \
        _get_holistic_and_congruent_date_time_vector_of_all_batches(dfs_batch_bin_rtn)
    date_cols = [col for col in dfs_batch_bin_rtn[0].columns if col.startswith("date")]
    for i, df in enumerate(dfs_batch_bin_rtn):
        df = df.drop(labels=date_cols, axis="columns")
        dfs_batch_bin_rtn[i] = df
    return dfs_batch_bin_rtn


def _get_holistic_and_congruent_date_time_vector_of_all_batches(dfs_batch_bin):
    date_time_vect = dfs_batch_bin[0].index.to_series()
    date_0 = date_time_vect[0].date()
    for i_df_x, df_x in enumerate(dfs_batch_bin[1:]):
        date_x = df_x.index[0].date()
        time_delta = date_x - date_0
        df_x_index_adapted = (df_x.index - time_delta).to_series()
        date_time_vect = date_time_vect.combine_first(df_x_index_adapted)

    df_nan = pd.DataFrame(np.NaN, index=date_time_vect, columns=dfs_batch_bin[0].columns)
    len_df_nan = len(df_nan)
    for i_df_x, df_x in enumerate(dfs_batch_bin):
        date_x = df_x.index[0].date()
        time_delta = date_x - date_0
        df_x_index_adapted = date_time_vect + time_delta
        df_nan.index = df_x_index_adapted
        df_x = df_x.combine_first(df_nan)
        assert(len(df_x) == len_df_nan)
        dfs_batch_bin[i_df_x] = df_x
    return dfs_batch_bin


def get_min_and_max_day_time_of_all_batches_dfs(dfs_batch_bin):
    min_time = dt.time(23, 59)
    max_time = dt.time(0, 0)
    for k in sorted(dfs_batch_bin.keys()):
        batched_dfs = dfs_batch_bin[k]
        (c_min_time, c_max_time) = get_min_and_max_day_time_of_multiple_dfs(batched_dfs)
        if c_min_time < min_time:
            min_time = c_min_time
        if c_max_time > max_time:
            max_time = c_max_time
    return (min_time, max_time)
