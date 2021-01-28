
import datetime as dt


def get_min_and_max_date_of_multiple_dfs(dfs):
    (min_time, max_time) = get_min_and_max_day_time_of_multiple_dfs(dfs)
    min_date = max(d.index[0] for d in dfs)
    min_date = dt.datetime.combine(min_date.date(), min_time)
    max_date = min(d.index[-1] for d in dfs)
    max_date = dt.datetime.combine(max_date.date(), max_time)
    return (min_date, max_date)


def get_min_and_max_day_time_of_multiple_dfs(dfs):
    min_time = max_time = None
    for df in dfs:
        dfs_splitted_in_days = [group[1] for group
                                in df.groupby([df.index.year, df.index.month, df.index.day])]
        min_time_x = min(dfx.index[0].time() for dfx in dfs_splitted_in_days)
        max_time_x = max(dfx.index[-1].time() for dfx in dfs_splitted_in_days)
        if min_time is None or min_time_x < min_time:
            min_time = min_time_x
        if max_time is None or max_time_x > max_time:
            max_time = max_time_x
    return (min_time, max_time)
