
import datetime
import requests
import urllib.parse
import json

from fetch_daily._polygon import _convert


def fetch_stock_data(symbol, start_date=None, end_date=None):
    # api-key _9OLGNWHtV6TQU4GKdzKx65sgDvOtvpm

    # sample requests S&P 500:
    #   https://api.polygon.io/v2/aggs/ticker/SPY/range/30/minute/2020-11-.19/2020-11-19?sort=asc&limit=10&apiKey=_9OLGNWHtV6TQU4GKdzKx65sgDvOtvpm

    if start_date is None:
        start_date = datetime.date.today()
    start_date = _convert.datetime_to_str(start_date)
    if end_date is not None:
        end_date = _convert.datetime_to_str(end_date)

    API_KEY = "_9OLGNWHtV6TQU4GKdzKx65sgDvOtvpm"

    symbol = urllib.parse.quote(symbol)

    url = "https://api.polygon.io/v2/aggs/ticker/SPY/range/5/minute/2020-11-19/2020-11-19?unadjusted=true&sort=asc&limit=150&apiKey=_9OLGNWHtV6TQU4GKdzKx65sgDvOtvpm"

    querystring = dict(region="US",
                       comparisons="%5EGDAXI%2C%5EFCHI",
                       symbol=symbol,
                       interval="5m",
                       range="1d",
                       )

    # Regarding parameters: period1; period2 > Wrong API description > Does not work

    response = requests.request("GET", url)
    txt = response.text
    resp_dict = json.loads(txt)
    resp_dict_list = _convert.to_adjusted_dict_list(resp_dict)
    return resp_dict_list


if __name__ == "__main__":
    fetch_stock_data("SPY")
