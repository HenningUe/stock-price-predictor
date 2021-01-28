
import datetime as dt

from _misc_frogs import datetime_helper
from _misc_frogs.loggermod import get_logger


def check_if_current_time_is_outside_trading_hours(symbol, extended_traiding_hours=True):
    if extended_traiding_hours:
        min_time = dt.time(hour=4)
        max_time = dt.time(hour=22, minute=30)
    else:
        min_time = dt.time(hour=8)
        max_time = dt.time(hour=16, minute=30)
    ny_time = datetime_helper.get_datetime_adapted_to_us_ny_time(dt.datetime.now())
    if ny_time.time() > min_time or ny_time.time() < max_time:
        msg = (f"Values for '{symbol}' can only be read at the end "
               f"of the trading opening time of the same day. "
               f"As the trading is still ongoing you only get "
               f"a part of the values")
        get_logger().warning(msg)
