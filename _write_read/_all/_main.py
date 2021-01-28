
import datetime
import pandas as pd
from pandas.tseries.offsets import BDay

from _misc_frogs.environment import get_data_source_root_folder

_DATETIME_CONV = "%Y/%m/%d %H:%M:%S"


def datetime_to_str(datetime_in):
    global _DATETIME_CONV
    if not isinstance(datetime_in, datetime.datetime):
        raise ValueError()
    return datetime_in.strftime(_DATETIME_CONV)


def str_to_datetime(datetime_in_str):
    global _DATETIME_CONV
    assert(isinstance(datetime_in_str, str))
    return datetime.datetime.strptime(datetime_in_str, _DATETIME_CONV)


def get_checked_date_parameters(date_start=None, date_end=None, time_range=None):  # @NOSONAR
    if date_start is not None and date_end is not None and time_range is not None:
        raise ValueError("Either must be None")
    if time_range is not None:
        if time_range.days < 1:
            raise ValueError("time_range must be equal or bigger 1")
    if date_start is not None and date_end is not None \
       and date_start > date_end:
        raise ValueError("date_start must be equal or smaller date_end")

    if date_end is None and date_start is not None and time_range is not None:
        date_end = date_start
        while True:
            day_delta = pd.date_range(date_start, date_end, freq=BDay())
            if time_range.days <= len(day_delta):
                break
            date_end += datetime.timedelta(days=1)
    if date_start is None and date_end is not None and time_range is not None:
        date_start = date_end
        while True:
            day_delta = pd.date_range(date_start, date_end, freq=BDay())
            if time_range.days <= len(day_delta):
                break
            date_start -= datetime.timedelta(days=1)

    return (date_start, date_end)


class FileNFolderProvider:

    def __init__(self, symbol, data_segmentation_type):
        self.symbol = symbol
        self.data_segmentation_type = data_segmentation_type

    def get_folder(self, postfix=""):
        rdir = get_data_source_root_folder()
        return rdir.joinpath(self.data_segmentation_type, self.symbol + postfix)
