
import datetime

from fetch_daily import _iexcloud2


def test():
    data = _iexcloud2.fetch_stock_data("SPY", datetime.date.today() - datetime.timedelta(days=1))


if __name__ == "__main__":
    test()
