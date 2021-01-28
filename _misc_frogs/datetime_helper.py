
import pytz
import datetime


def get_datetime_adapted_to_us_ny_time(datetime_in_german_time):
    germany = pytz.timezone('Europe/Berlin')
    us_ny = pytz.timezone('America/New_York')
    germany_time = germany.localize(datetime_in_german_time, is_dst=False)
    us_ny_time = us_ny.localize(datetime_in_german_time, is_dst=False)
    delta_time = germany_time - us_ny_time
    delta_hours = int(delta_time.total_seconds() / 60 / 60)
    delta_time = datetime.timedelta(seconds=delta_hours * 60 * 60)
    rtn_time = germany_time + delta_time
    return rtn_time


def get_us_ny_00h_timestamp_for_date_x(date_x):
    us_ny = pytz.timezone('America/New_York')
    as_datetime = datetime.datetime.fromordinal(date_x.toordinal())
    us_ny_datetime = us_ny.localize(as_datetime, is_dst=False)
    return int(us_ny_datetime.timestamp())


if __name__ == "__main__":
    t = get_datetime_adapted_to_us_ny_time(datetime.datetime.now())
    f = 1
