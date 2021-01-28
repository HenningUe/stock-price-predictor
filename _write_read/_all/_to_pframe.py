
import pandas as pd


def to_pandas_dataframe(dict_list):
    if isinstance(dict_list, dict):
        df = _to_pandas_dataframe_from_dict_of_lists(dict_list)
    else:
        df = _to_pandas_dataframe_from_list_of_dicts(dict_list)
    df.index = df.time
    df = df.drop(labels=['time'], axis="columns")
    return df


def _to_pandas_dataframe_from_dict_of_lists(dict_of_lists):
    time_series = dict_of_lists.pop('time')
    df = pd.DataFrame.from_dict(dict_of_lists)
    df['time'] = pd.to_datetime(time_series)
    return df


def _to_pandas_dataframe_from_list_of_dicts(list_of_dicts):
    df = pd.DataFrame(list_of_dicts)
    if 'open' not in df.columns:
        df = df.transpose()
    df['time'] = pd.to_datetime(df.time)
    return df
