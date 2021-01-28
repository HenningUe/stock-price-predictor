
import json
import datetime
from datetime import timedelta

from _misc_frogs import errors
from _misc_frogs.pd_dataframes.resample import resample_pframe_to_x_minutes_filling_with_zeros

from .._all import (FileNFolderProvider, get_checked_date_parameters,
                    datetime_to_str, str_to_datetime)
from .._all import to_pandas_dataframe


def write_data_for_day(symbol, data):
    file_handler = SingleFileHandler(symbol)
    file_handler.write(data)


def get_data_from_date_range(symbol, date_start=None, date_end=None, time_range=None):
    data = list()
    file_handler = SingleFileHandler(symbol)
    (date_start, date_end) = get_checked_date_parameters(date_start, date_end, time_range)
    if date_start is None:
        date_start = file_handler.get_first_date()
    if date_end is None:
        date_end = file_handler.get_last_date()
    while True:
        try:
            new_data = file_handler.read(date_start)
        except FileNotFoundError:
            raise errors.DataPointMissingError(date_start)
        data.extend(new_data)
        while True:
            date_start += datetime.timedelta(days=1)
            if date_start.weekday() < 5:
                break
        if date_start > date_end:
            break
    return data


def get_data_from_date_range_as_dframe(symbol, date_start=None, date_end=None, time_range=None):
    data_raw = get_data_from_date_range(symbol, date_start, date_end, time_range)
    df = to_pandas_dataframe(data_raw)
    df = resample_pframe_to_x_minutes_filling_with_zeros(df)
    return df


def get_data_from_day(symbol, date=None):
    if date is None:
        date = datetime.date.today()
    return get_data_from_date_range(symbol, date_start=date, time_range=timedelta(days=1))


def get_data_from_day_as_dframe(symbol, date=None):
    if date is None:
        date = datetime.date.today()
    return get_data_from_date_range_as_dframe(symbol, date_start=date, time_range=timedelta(days=1))


class SingleFileHandler:

    def __init__(self, symbol):
        self._fnf_provider = FileNFolderProvider(symbol, "all_in_multiple")

    def read(self, datetime_in):
        data_as_json = self._get_filepath(datetime_in).read_text()
        data = json.loads(data_as_json)
        for item in data:
            item['time'] = str_to_datetime(item['time'])
        return data

    def write(self, data_in):
        data_in_0 = data_in[0]
        date = data_in_0['time']
        for item in data_in:
            item['time'] = datetime_to_str(item['time'])
        data_as_json = json.dumps(data_in, indent=4)
        storage_file = self._get_filepath(date)
        if not storage_file.parent.is_dir():
            storage_file.parent.mkdir(parents=True)
        self._get_filepath(date).write_text(data_as_json)

    def _get_filepath(self, datetime_in):
        date_str = datetime_in.strftime("%Y_%m_%d")
        file_name = date_str + ".json"
        storage_dir = self._fnf_provider.get_folder()
        return storage_dir.joinpath(file_name)

    def get_first_date(self):
        rtn = self._get_first_and_last_date()
        return rtn['first_date']

    def get_last_date(self):
        rtn = self._get_first_and_last_date()
        return rtn['last_date']

    def _get_first_and_last_date(self):
        files = [f.name.lower() for f
                 in self._fnf_provider.get_folder().glob("*.json")]
        files.sort()
        first_date = files[0].split(".")[0]
        first_date = datetime.datetime.strptime(first_date, "%Y_%m_%d")
        last_date = files[0].split(".")[0]
        last_date = datetime.datetime.strptime(last_date, "%Y_%m_%d")
        return dict(first_date=first_date,
                    last_date=last_date)
