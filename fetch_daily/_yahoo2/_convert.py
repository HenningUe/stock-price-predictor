
from datetime import datetime


def to_adjusted_dict_list(yahoo_inputdata):
    timestamp_list = _get_parsed_time_stamp_list(yahoo_inputdata)
    data = _get_parsed_values(yahoo_inputdata)
    rtn_data = list()
    for i, time_st in enumerate(timestamp_list):
        value_dict = dict(time=time_st,
                          volume=data['volume'][i],
                          open=data['open'][i],
                          close=data['close'][i],
                          high=data['high'][i],
                          low=data['low'][i],
                          )
        rtn_data.append(value_dict)
    return rtn_data


def _get_parsed_time_stamp_list(inputdata):
    timestamp_list = inputdata["chart"]["result"][0]["timestamp"]
    timestamp_list = [datetime.fromtimestamp(ts) for ts in timestamp_list]
    return timestamp_list


def _get_parsed_values(inputdata):
    value_dict = dict()
    'volume', 'open', 'high', 'close', 'low'
    value_dict['volume'] = inputdata["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
    value_dict['open'] = inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"]
    value_dict['close'] = inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    value_dict['high'] = inputdata["chart"]["result"][0]["indicators"]["quote"][0]["high"]
    value_dict['low'] = inputdata["chart"]["result"][0]["indicators"]["quote"][0]["low"]
    return value_dict
