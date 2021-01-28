
import datetime
import re

_DATETIME_CONV = "%Y-%m-%d %H:%M:%S"


def to_adjusted_dict_list(aphavantage_inputdata):
    KEY_CLEAR = re.compile("\d+\. (\w+)")
    series_keys = [k for k in aphavantage_inputdata.keys()
                   if not k.lower() == "meta data"]
    series_key = series_keys[0]
    series_as_dict = aphavantage_inputdata[series_key]
    series = list()
    for k_time in series_as_dict:
        item_ = series_as_dict[k_time]
        item = {KEY_CLEAR.match(k).group(1): item_[k] for k in item_}
        item['time'] = str_to_datetime(k_time)
        series.append(item)
    return series


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


if __name__ == "__main__":
    import json
    with open("test_data.txt") as f:
        txt = f.read()
    as_dict = json.loads(txt)
    as_list = to_adjusted_dict_list(as_dict)
    print(as_list)
