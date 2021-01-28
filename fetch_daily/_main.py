
import datetime

from _misc_frogs.loggermod import get_logger
import _write_read

from . import _iexcloud2, _twelvedata2, _yahoo2, _alphavantage  # @UnusedImport

# description:
#  yahoo > provides S&P Mini-Future
#  _alphavantage > provides S&P SPY extended trading hours
#  futures incl.; guter Preis 20,-/Montag, extend trading hours.. nachfragen


def run_daily_fetch():
    rtn_data = dict()
    SYMBOLS = [
               dict(provider='yahoo', symb="ES=F", descr="S&P500 MiniFuture Continuous"),
               dict(provider='alphavantage', symb="SPY", descr="SPDR S&P 500 ETF Trust"),
               # dict(provider='twelvedata', symb="SPY", descr="SPDR S&P 500 ETF Trust"),
               # dict(provider='yahoo', symb="SPY", descr="SPDR S&P 500 ETF Trust"),
               ]

    success_collect = list()
    for symb_dict in SYMBOLS:
        try:
            symb_data = _run_daily_fetch_single_symbol(symb_dict)
            success_collect.append(symb_dict['symb'])
        except Exception as ex:
            fargs = {**symb_dict, **dict(ex=ex)}
            msg = ("Error occurred at fetching data:\n"
                   "Provider: {provider}; Symbol: {symb}\n"
                   "Error message:\n{ex}".format(**fargs))
            get_logger().warning(msg)
        else:
            rtn_data[symb_dict['symb']] = symb_data
            get_logger().info("Collected data for: {}".format(", ".join(success_collect)))
    return rtn_data


def _run_daily_fetch_single_symbol(symb_dict):
    date_yesterday = datetime.date.today() - datetime.timedelta(days=1)
    symbol = symb_dict['symb']
    provider = symb_dict['provider']
    if provider == "yahoo":
        symb_data = _yahoo2.fetch_stock_data(symbol)
    elif provider == "twelvedata":
        symb_data = _twelvedata2.fetch_stock_data(symbol, date_yesterday)
    elif provider == "iexcloud":
        symb_data = _iexcloud2.fetch_stock_data(symbol, date_yesterday)
    elif provider == "alphavantage":
        symb_data = _alphavantage.fetch_stock_data(symbol)
    else:
        raise NotImplementedError()
    _write_read.all_in_multiple.write_data_for_day(symbol, symb_data)
    return symb_data
