

import datetime as dt
import pandas as pd
# import numpy as np

from .analysing import get_min_and_max_day_time_of_multiple_dfs, get_min_and_max_date_of_multiple_dfs


def make_dataframes_min_max_dates_equal(symbols_data):
    dfs = [d['df'] for d in symbols_data]
    (min_date, max_date) = get_min_and_max_date_of_multiple_dfs(dfs)
    for symb_data in symbols_data:
        symb_data['df'] = symb_data['df'].truncate(
            before=min_date, after=max_date)
    return symbols_data


def make_dataframe_days_equally_long(dfs):
    is_list_of_dfs = True
    if isinstance(dfs, pd.DataFrame):
        is_list_of_dfs = False
        dfs = [dfs]
    (min_time, max_time) = get_min_and_max_day_time_of_multiple_dfs(dfs)
    for i, df in enumerate(dfs):
        df_new = make_dataframe_days_equally_long_of_single_df(df, min_time, max_time)
        dfs[i] = df_new
    if not is_list_of_dfs:
        dfs = dfs[0]
    return dfs


def make_dataframe_days_equally_long_of_single_df(df, min_time, max_time):
    TARGET_SAMPLE_PERIOD_IN_MIN = 5
    col_names = [c for c in df.columns]
    dfs_splitted_in_days = [group[1] for group
                            in df.groupby([df.index.year, df.index.month, df.index.day])]

    for i_df_x, df_x in enumerate(dfs_splitted_in_days):
        # (len(df_x) - 2) > -2 to ensure, that sample_period is above 1
        try:
            is_sample_period_in_sec = (
                df_x.index[-1] - df_x.index[0]) / (len(df_x) - 2)
        except Exception as ex:
            x = 1
        is_sample_period_in_min = int(
            is_sample_period_in_sec.total_seconds() / 60)
        assert ((TARGET_SAMPLE_PERIOD_IN_MIN % is_sample_period_in_min) == 0)

        df_first = _create_empty_dataframe_from_to_date(col_names, min_time, df_x.index[0],
                                                        TARGET_SAMPLE_PERIOD_IN_MIN)
        df_after = _create_empty_dataframe_from_to_date(col_names, df_x.index[-1], max_time,
                                                        TARGET_SAMPLE_PERIOD_IN_MIN)
        if df_first is None:
            df_first = df_x
        else:
            df_first = df_first.append(df_x)
        if df_after is not None:
            df_first = df_first.append(df_after)
        dfs_splitted_in_days[i_df_x] = df_first

    df = dfs_splitted_in_days[0]
    df = df.append(dfs_splitted_in_days[1:])
    df = _remove_duplicated_index_elements(df)
    return df


def _remove_duplicated_index_elements(df):
    df = df.loc[~df.index.duplicated()]
    return df


def _create_empty_dataframe_from_to_date(column_names, start_time, end_time, freq_in_min):
    if isinstance(start_time, dt.time):
        start_time = dt.datetime.combine(end_time.date(), start_time)
    elif isinstance(end_time, dt.time):
        end_time = dt.datetime.combine(start_time.date(), end_time)
    duration = end_time - start_time
    periods = int(duration.total_seconds() / freq_in_min / 60)
    if periods == 0:
        return None
    else:
        start_time += dt.timedelta(seconds=freq_in_min * 60)
        date_col = pd.Series(pd.date_range(
            start_time, freq=f"{freq_in_min}Min", periods=periods))
        df = pd.DataFrame(columns=column_names, index=date_col)
        return df


if __name__ == "__main__":
    time_col = pd.Series(pd.date_range('2000', freq='D', periods=3))
    df = pd.DataFrame(columns=['a', 'b'], index=time_col)
    x = 1
