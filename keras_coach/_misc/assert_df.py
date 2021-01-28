

def assert_dfs(dfs):
    if not isinstance(dfs, list):
        dfs = [dfs]
    for df in dfs:
        assert_df(df)


def assert_df(df):
    return
    TRESHOLD = 1000
    try:
        if df.maxmin_diff.max() > TRESHOLD:
            raise AssertionError("maxmin.max")
        if df.maxmin_diff.min() < -TRESHOLD:
            raise AssertionError("maxmin.min")
        if df.open.max() > TRESHOLD:
            raise AssertionError("open.max")
        if df.open.min() < -TRESHOLD:
            raise AssertionError("open.min")
        if df.close.max() > TRESHOLD:
            raise AssertionError("close.max")
        if df.close.min() < -TRESHOLD:
            raise AssertionError("close.min")
        if df.volume.max() > TRESHOLD:
            raise AssertionError("volume.max")
        if df.volume.min() < -TRESHOLD:
            raise AssertionError("volume.min")
        if 'maxmin_diff_0' in df.columns:
            if df.maxmin_diff_0.max() > TRESHOLD:
                raise AssertionError("maxmin_0.max")
            if df.maxmin_diff_0.min() < -TRESHOLD:
                raise AssertionError("maxmin_0.min")
            if df.open_0.max() > TRESHOLD:
                raise AssertionError("open_0.max")
            if df.open_0.min() < -TRESHOLD:
                raise AssertionError("open_0.min")
            if df.close_0.max() > TRESHOLD:
                raise AssertionError("close_0.max")
            if df.close_0.min() < -TRESHOLD:
                raise AssertionError("close_0.min")
            if df.volume_0.max() > TRESHOLD:
                raise AssertionError("volume_0.max")
            if df.volume_0.min() < -TRESHOLD:
                raise AssertionError("volume_0.min")

    except Exception as ex:
        x = 1
