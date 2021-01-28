
import datetime as dt
import pandas as pd
import numpy as np

from ._helper import time_add


def filter_out_df_batches_with_unusable_days(df_batches, vector_with_not_usable_days):
    df_with_not_usable_days = pd.DataFrame(
        vector_with_not_usable_days, columns=list(['date', ]))
    df_with_not_usable_days.index = pd.RangeIndex(
        0, len(df_with_not_usable_days))

    def _get_date(series_in): return series_in.index[0].date()  # @IgnorePep8

    filtered_df_batches = list()
    for batch in df_batches:
        df = batch['df']
        df['date'] = df.index
        df_group = df.groupby([df.index.year, df.index.month, df.index.day]).agg(
            {'date': _get_date})
        df_group.index = pd.RangeIndex(0, len(df_group))
        df_group_not_usable_days = pd.merge(
            df_group, df_with_not_usable_days, on='date', how='inner')
        if df_group_not_usable_days.empty:
            df = df.drop(labels=['date'], axis='columns')
            filtered_df_batches.append(batch)
    return filtered_df_batches


def get_time_vector_containing_not_usable_days(symbols_data):
    validation_dfs = list()
    for symb in symbols_data:
        day_start_time = symb['spec']['day_start_time']
        day_end_time = symb['spec']['day_end_time']
        df = _get_validation_df_for_single_symbol(symb['df'], day_start_time, day_end_time)
        validation_dfs.append(df)
    vect_with_unusable_days = \
        _get_unusable_df_vector_from_validation_dfs(validation_dfs)
    for symb in symbols_data:
        symb['df'] = symb['df'].drop(['is_valid', 'date'], axis='columns')
    return np.array(vect_with_unusable_days)


def _get_validation_df_for_single_symbol(df, day_start_time, day_end_time):
    min_time = time_add(day_start_time, dt.timedelta(minutes=45))
    max_time = time_add(day_end_time, -dt.timedelta(minutes=45))

    def _is_in_valid_time_range(series_in):
        return (series_in.index[0].time() < min_time and series_in.index[-1].time() > max_time)

    def _get_date_from_datetime(series_in):
        return series_in.index[0].date()

    df['is_valid'] = df.index
    df['date'] = df.index
    df_group = df.groupby([df.index.year, df.index.month, df.index.day])
    df_c = df_group.agg(
        {'is_valid': _is_in_valid_time_range,
         'date': _get_date_from_datetime})
    df_c = df_c[~df_c.is_valid]  # @IgnorePep8
    return df_c


def _get_unusable_df_vector_from_validation_dfs(dfs):
    df_merged = None
    for df in dfs:
        if df_merged is None:
            df_merged = df[(df.is_valid != True)]  # @IgnorePep8
            continue
        df_merged = pd.merge(df, df_merged, left_on='date',
                             right_on='date', how='outer', suffixes=('', '_1',))
        df_merged = df_merged[(df_merged.is_valid != True)  # @IgnorePep8
                              | (df_merged.is_valid_1 != True)]  # @IgnorePep8
        df_merged = df_merged.drop(['is_valid_1'], axis='columns')
        df_merged.is_valid = df_merged.is_valid.replace(True, False)
        df_merged.is_valid = df_merged.is_valid.replace(np.NaN, False)
    return df_merged.date

    # def _get_time_vector_containing_not_usable_days_old(dfs):
    #     min_time = time_add(min_time, dt.timedelta(minutes=10))
    #     max_time = time_add(max_time, -dt.timedelta(minutes=10))
    #
    #     def _is_in_valid_time_range(series_in):
    #         return (series_in.index[0].time() < min_time and series_in.index[-1].time() > max_time)
    #
    #     def _get_date_from_datetime(series_in):
    #         return series_in.index[0].date()
    #
    #     df_merged = None
    #     for df in dfs:
    #         df['is_valid'] = df.index
    #         df['date'] = df.index
    #         df_group = df.groupby([df.index.year, df.index.month, df.index.day])
    #         df_c = df_group.agg(
    #             {'is_valid': _is_in_valid_time_range, 'date': _get_date_from_datetime})
    #         if df_merged is None:
    #             df_merged = df_c[(df_c.is_valid != True)]  # @IgnorePep8
    #             continue
    #         df_merged = pd.merge(df_c, df_merged, left_on='date',
    #                              right_on='date', how='outer', suffixes=('', '_1',))
    #         df_merged = df_merged[(df_merged.is_valid != True) | (
    #             df_merged.is_valid_1 != True)]  # @IgnorePep8
    #         df_merged = df_merged.drop(['is_valid_1'], axis='columns')
    #         df_merged = df_merged.is_valid.replace(True, False)
    #         df_merged = df_merged.is_valid.replace(np.NaN, False)
    #     for df in dfs:
    #         df.drop(['is_valid'], axis='columns', inplace=True)
    #     return df_merged.date
