
import numpy as np


def resample_pframe_to_x_minutes_filling_with_zeros(df, sample_period_in_min):
    DOWNSAMPLE_COLS_AGGRE_FUNC_DEFS = dict(open='last', close='last',
                                           low='last', high='last', volume='sum')
    RESAMPLE_VAL = f"{sample_period_in_min}Min"
    df = df.resample(RESAMPLE_VAL).agg(DOWNSAMPLE_COLS_AGGRE_FUNC_DEFS)
    return df


def downsample_pframe_to_x_minutes(df, sample_period_in_min=5, allowed_delta_percentage=None):
    dfs_splitted_in_days = [group[1] for group
                            in df.groupby([df.index.year, df.index.month, df.index.day])]
    mean_len = None
    for i_df_x, df_x in enumerate(dfs_splitted_in_days):
        cur_len = len(df_x)
        mean_len = cur_len if mean_len is None else (mean_len + cur_len) / 2
        if allowed_delta_percentage is not None \
           and abs(cur_len - mean_len) / mean_len > allowed_delta_percentage / 100:
            raise ValueError(f"Each day must have same similar amount of values "
                             f"(+- {allowed_delta_percentage}%). "
                             f"Error at {str(df_x.time[0].date())}")
        if cur_len < 2:
            raise ValueError(f"Each day must have a len > 1. "
                             f"Error at {str(df_x.time[0].date())}")

        if 'time' in df_x.columns:
            df_x.index = df_x.time
        df_x = resample_pframe_to_x_minutes_filling_with_zeros(df_x, sample_period_in_min)
        dfs_splitted_in_days[i_df_x] = df_x

    df = dfs_splitted_in_days[0]
    df = df.append(dfs_splitted_in_days[1:])
    return df
