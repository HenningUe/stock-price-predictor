import datetime

import _init  # @UnresolvedImport @UnusedImport

import fetch_daily
import _write_read


def main():
    date_yesterday = datetime.date.today() - datetime.timedelta(days=1)
    # fetch_daily.run_daily_fetch()
    # data_spy = _write_read.all_in_multiple.get_data_from_day_as_dframe(symbol="SPY", date=date_yesterday)
    data_ef_s = _write_read.all_in_multiple.get_data_from_day_as_dframe(symbol="ES=F", date=date_yesterday)
    x = 1


main()
