import datetime

import _init  # @UnresolvedImport @UnusedImport

import _write_read


def main():
    fetch_end_date = datetime.date(year=2020, month=11, day=13)
    time_range = datetime.timedelta(days=13)
    data = _write_read.all_in_one.get_data_from_date_range(symbol="SPY",
                                                           date_end=fetch_end_date,
                                                           time_range=time_range)
    x = 1


main()
