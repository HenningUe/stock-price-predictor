
import requests
import urllib.parse
import json

from .. import _common
from . import _convert


def fetch_stock_data(symbol):
    _common.check_if_current_time_is_outside_trading_hours(symbol)

    API_KEY = "LU4GPP2MU43TL2SP"
    symbol = urllib.parse.quote(symbol)

    # outputsize = int((20 - 4) * 60 / 5)  # trading 4h - 20h, 5 min data range

    querystring = dict(function="TIME_SERIES_INTRADAY",
                       symbol=symbol,
                       interval="5min",
                       outputsize="full",
                       apikey=API_KEY
                       )

    # Regarding parameters: period1; period2 > Wrong API description > Does not work
    URL = "https://www.alphavantage.co/query"
    response = requests.request("GET", URL, params=querystring)
    txt = response.text
    resp_dict = json.loads(txt)
    data = _convert.to_adjusted_dict_list(resp_dict)
    return data


if __name__ == "__main__":
    fetch_stock_data("SPY")
