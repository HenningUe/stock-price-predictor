
import requests
import urllib.parse
import json

from .. import _common
from . import _convert


def fetch_stock_data(symbol):
    _common.check_if_current_time_is_outside_trading_hours(symbol)

    # https://rapidapi.com/blog/yahoo-finance-api-python/
    RAPIDAPI_KEY = "dcf0b727edmsh0e54c3c5fe83825p18abe4jsn85d620f6ee9d"
    symbol = urllib.parse.quote(symbol)

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts"

    querystring = dict(region="US",
                       comparisons="%5EGDAXI%2C%5EFCHI",
                       symbol=symbol,
                       interval="5m",
                       range="1d",
                       )

    # Regarding parameters: period1; period2 > Wrong API description > Does not work

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPIDAPI_KEY
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    txt = response.text
    resp_dict = json.loads(txt)
    resp_dict_list = _convert.to_adjusted_dict_list(resp_dict)
    return resp_dict_list
