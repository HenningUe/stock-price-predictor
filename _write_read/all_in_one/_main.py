
import datetime as dt
from datetime import timedelta
import pathlib
import pandas as pd

from _misc_frogs.pd_dataframes.resample import downsample_pframe_to_x_minutes
from _misc_frogs.pd_dataframes.normalize import normalize_stock_price

from .._all import FileNFolderProvider, get_checked_date_parameters
from .._all import persist, load, data_exists


def process_and_store_global_key_data_items(symbol, date_start=None):
    if date_start is None:
        date_start = dt.date(2005, 1, 1)
    df = get_data_from_date_range_as_dframe(symbol, date_start=date_start)
    data = dict()
    price_normalized = normalize_stock_price(df.open)
    data['open_std'] = price_normalized.std()
    data['open_mean'] = price_normalized.mean()
    price_normalized = normalize_stock_price(df.close)
    data['close_std'] = price_normalized.std()
    data['close_mean'] = price_normalized.mean()
    maxmin_diff = (df.high - df.low) / df.low
    data['maxmin_diff_std'] = maxmin_diff.std()
    data['maxmin_diff_mean'] = maxmin_diff.mean()
    persist(symbol, data)


def read_global_key_data_items(symbol):
    if not data_exists(symbol):
        process_and_store_global_key_data_items(symbol)
    return load(symbol)


def get_data_from_date_range(symbol, date_start=None, date_end=None, time_range=None):
    df = get_data_from_date_range_as_dframe(
        symbol, date_start, date_end, time_range)
    data = df.to_dict(orient='records')
    return data


def get_data_from_date_range_as_dframe(symbol, date_start=None, date_end=None, time_range=None, resample_df=True):
    (date_start_x, date_end_x) = get_checked_date_parameters(
        date_start, date_end, time_range)
    file_handler = FileHandlerFirstRateData(symbol)
    df = file_handler.read(date_start_x, date_end_x)
    df = _get_data_filtered_by_date_range(df, date_start, date_end, time_range)
    if resample_df:
        df = downsample_pframe_to_x_minutes(df)
    return df


def get_daydeltas_from_date_range_as_dframe(symbol, date_start=None, date_end=None, time_range=None):
    # Returns relative difference between day's start and end price, related
    # to start price
    df = get_data_from_date_range_as_dframe(
        symbol, date_start, date_end, time_range)

    dfs_splitted_in_days = [group[1] for group
                            in df.groupby([df.index.year, df.index.month, df.index.day])]
    date_index = pd.date_range(start=df.index[0].date(
    ), periods=len(dfs_splitted_in_days), freq='B')
    df_return = pd.DataFrame(columns=['day_delta'], index=date_index)
    for i_df_x, df_x in enumerate(dfs_splitted_in_days):
        # (len(df_x) - 2) > -2 to ensure, that sample_period is above 1
        day_delta = (df_x.close[-1] - df_x.open[0]) / df_x.open[0]
        df_return.day_delta[i_df_x] = day_delta
    return df_return


def get_yahoo_daydeltas_from_date_range_as_dframe(symbol, date_start=None, date_end=None, time_range=None):
    file_handler = FileHandlerYahoo(symbol)
    df = file_handler.read()
    df = _get_data_filtered_by_date_range(df, date_start, date_end, time_range)
    dfs_splitted_in_days = [group[1] for group
                            in df.groupby([df.index.year, df.index.month, df.index.day])]
    date_index = pd.date_range(start=df.index[0].date(
    ), periods=len(dfs_splitted_in_days), freq='B')
    df_return = pd.DataFrame(columns=['day_delta'], index=date_index)
    for i_df_x, df_x in enumerate(dfs_splitted_in_days):
        # (len(df_x) - 2) > -2 to ensure, that sample_period is above 1
        day_delta = (df_x.close[-1] - df_x.open[0]) / df_x.open[0]
        df_return.day_delta[i_df_x] = day_delta
    return df_return


def get_data_from_day(symbol, date=None):
    if date is None:
        date = dt.date.today()
    return get_data_from_date_range(symbol, date_start=date, time_range=timedelta(days=1))


def get_data_from_day_as_dframe(symbol, date=None):
    if date is None:
        date = dt.date.today()
    return get_data_from_date_range_as_dframe(symbol, date_start=date, time_range=timedelta(days=1))


def _get_data_filtered_by_date_range(df, date_start=None, date_end=None, time_range=None):
    (date_start, date_end) = get_checked_date_parameters(
        date_start, date_end, time_range)
    if not (date_start is None and date_end is None):
        date_start_pd = None if date_start is None else pd.Timestamp(
            date_start)
        date_end_pd = None if date_end is None else pd.Timestamp(
            date_end + timedelta(days=1))
        date_start_filter = True if date_start_pd is None else df['time'] >= date_start_pd
        date_end_filter = True if date_end_pd is None else df['time'] <= date_end_pd
        filter_mask = date_start_filter & date_end_filter
        df = df.loc[filter_mask]
    return df


class FileHandlerFirstRateData:

    def __init__(self, symbol):
        self.symbol = symbol
        self._fnf_provider = FileNFolderProvider(symbol, "all_in_one")

    def read(self, date_start=None, date_end=None):
        cols = ['time', 'open', 'high', 'low', 'close', 'volume']
        df_out = None
        for f_paths in self._get_filepaths(date_start, date_end):
            df = pd.read_csv(f_paths, names=cols)
            df.time = pd.to_datetime(df.time, format="%Y-%m-%d  %H:%M:%S")
            df.index = df.time
            if df_out is None:
                df_out = df
            else:
                df_out = df_out.append(df)
        return df_out

    def _get_filepaths(self, date_start, date_end):
        p = pathlib.Path(self._fnf_provider.get_folder()
                         ).glob(f'{self.symbol}_*_*.txt')
        files = [x for x in p if x.is_file()]
        files.sort()
        files_to_read = list()
        for f in files:
            *_, first_y, last_y = f.with_suffix("").name.split("_")
            if date_start is not None and date_start.year > int(last_y):
                continue
            if date_end is not None and date_end.year < int(first_y):
                break
            files_to_read.append(f)
        return files_to_read


class FileHandlerYahoo:

    def __init__(self, symbol):
        self._fnf_provider = FileNFolderProvider(symbol, "all_in_one")

    def read(self):
        cols = ['time', 'open', 'high', 'low', 'close', 'adj_close', 'volume']
        df = pd.read_csv(self._get_filepath(), names=cols, header=0)
        df.time = pd.to_datetime(df.time, format="%Y-%m-%d")
        df.index = df.time
        return df

    def _get_filepath(self):
        file_name = "historical_data.csv"
        return pathlib.Path.joinpath(self._fnf_provider.get_folder("_yahoo"), file_name)
