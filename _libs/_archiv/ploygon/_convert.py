
import datetime

_DATETIME_CONV = "%Y-%m-%d %H:%M:%S"


def to_adjusted_dict_list(twelvedata_inputdata):
    for item in twelvedata_inputdata:
        item['time'] = item['datetime']
        item['time'] = str_to_datetime(item['time'])
        item.pop('datetime')
    return twelvedata_inputdata


def str_to_datetime(datetime_in_str):
    global _DATETIME_CONV
    assert(isinstance(datetime_in_str, str))
    return datetime.datetime.strptime(datetime_in_str, _DATETIME_CONV)


def datetime_to_str(datetime_in):
    global _DATETIME_CONV
    assert(isinstance(datetime_in, (datetime.datetime, datetime.date)))
    if isinstance(datetime_in, datetime.datetime):
        return datetime_in.strftime(_DATETIME_CONV)
    elif isinstance(datetime_in, datetime.date):
        return datetime_in.strftime(_DATETIME_CONV.split(" ")[0])
