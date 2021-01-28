
import requests
import urllib.parse
import json


def fetch_stock_data(symbol):

    symbol = urllib.parse.quote(symbol)
    symbol = "AAPL.US"

    url = f"https://eodhistoricaldata.com/api/real-time/{symbol}"

    querystring = dict(api_token="OeAFFmMliFG5orCUuwAKQ8l4WWFQ67YX",
                       fmt="json",
                       )

    # Regarding parameters: period1; peri

    response = requests.request("GET", url, params=querystring)
    txt = response.text
    resp_dict = json.loads(txt)
    return resp_dict


if __name__ == "__main__":
    fetch_stock_data("SPY")
