
import requests

# src = https://marketstack.com/product

# uekoetter@gmail.com
# vpqU8s356Y6dUaF

# API-key
# 743075c2a17ab5b689ab145e35120d70

# // Intraday Data API Endpoint
#
# http://api.marketstack.com/v1/intraday
#     ? access_key = YOUR_ACCESS_KEY
#     & symbols = AAPL
#
# // optional parameters:
#
#     & interval = 1h
#     & sort = DESC
#     & date_from = YYYY-MM-DD
#     & date_to = YYYY-MM-DD
#     & limit = 100
#     & offset = 0


def get_stock_data():
    params = dict(
      access_key='743075c2a17ab5b689ab145e35120d70',
      symbols="SPY",
      interval="15min",  # smaller not possible
      date_from='2020-11-24',
      date_to='2020-11-24',
    )

    api_result = requests.get('http://api.marketstack.com/v1/intraday', params)
    api_response = api_result.json()

    for stock_data in api_response['data']:
        print(u'Ticker %s has a day high of  %s on %s' % (
          stock_data['symbol'],
          stock_data['high'],
          stock_data['date'],)
    )


if __name__ == "__main__":
    get_stock_data()
