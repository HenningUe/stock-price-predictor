
import datetime as dt


def time_add(time, timedelta):
    start = dt.datetime(2000, 1, 1,
                        hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    return end.time()


def time_minus(time1, time2):
    time1_dt = dt.datetime(2000, 1, 1,
                           hour=time1.hour, minute=time1.minute, second=time1.second)
    time2_dt = dt.datetime(2000, 1, 1,
                           hour=time2.hour, minute=time2.minute, second=time2.second)
    return time1_dt - time2_dt
