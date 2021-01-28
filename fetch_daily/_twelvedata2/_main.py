
import datetime

from twelvedata import TDClient

from . import _convert


def fetch_stock_data(symbol, start_date=None, end_date=None):
    # https://twelvedata.com/docs#getting-started
    # api-key 149bea4934d04a67b668e4d9799e72eb

    # sample requests S&P 500:
    #   https://api.twelvedata.com/time_series?symbol=SPX&interval=1h&apikey=149bea4934d04a67b668e4d9799e72eb
    #   https://api.twelvedata.com/time_series?symbol=ES=F&interval=5min&exchange=NYSE&type=stock&format=JSON&apikey=149bea4934d04a67b668e4d9799e72eb
    #   https://api.twelvedata.com/time_series?symbol=ES=F&interval=1h&apikey=149bea4934d04a67b668e4d9799e72eb

    if start_date is None:
        start_date = datetime.date.today()
    start_date = _convert.datetime_to_str(start_date)
    if end_date is not None:
        end_date = _convert.datetime_to_str(end_date)

    API_KEY = "149bea4934d04a67b668e4d9799e72eb"

    td = TDClient(apikey=API_KEY)
    args = dict(
        symbol=symbol,
        exchange="NASDAQ",
        interval="5min",
        timezone="America/New_York",
        start_date=start_date,
        outputsize=288,  # 79,
    )
    if end_date is not None:
        args.update(dict(end_date=end_date))
    ts = td.time_series(**args)
    # WMA = Weighted Moving Average (WMA)
    # Returns: OHLC, BBANDS(close, 20, 2, EMA), PLUS_DI(9), WMA(20), WMA(40)
    # ts.with_bbands(ma_type="EMA").with_plus_di().with_wma(time_period=20).with_wma(time_period=40).as_pandas()

    as_dict_list = ts.as_json()
    as_dict_list = _convert.to_adjusted_dict_list(as_dict_list)
    return as_dict_list
