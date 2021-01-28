
# import numpy as np

# import _write_read
# from _misc_frogs.pd_dataframes.normalize import normalize_column
from _misc_frogs.pd_dataframes.normalize import normalize_stock_price
from keras_coach._misc import assert_df


def get_dataframe_with_normalized_training_data_over_complete_range(df):
    df = get_max_min_diff_normalized(df)
    return df


def get_dataframe_with_normalized_training_data_for_dataset_batches(df_batches):
    for i, batch in enumerate(df_batches):
        df = batch['df']
        df = get_volume_normalized(df)
        df = get_stock_prices_normalized(df, 'relative_to_first_batch_price')
        assert_df.assert_df(df)
        df_batches[i]['df'] = df
    return df_batches


def get_max_min_diff_normalized(df):
    relative_maxmin_diff = (df.high - df.low) / df.low
    relative_maxmin_diff_norm = relative_maxmin_diff - relative_maxmin_diff.mean(axis=0)
    relative_maxmin_diff_norm /= relative_maxmin_diff_norm.std(axis=0)
    df['maxmin_diff'] = relative_maxmin_diff_norm
    df = df.drop(labels=['high', 'low'], axis='columns')
    return df


def get_volume_normalized(df):
    # IDEE:
    # Volumen muss relativiert werden, da bei steigenden Aktienkursen auch die Umsaetze
    # steigen. Zudem gibt es Wochen/Monatsweise hoehere Volumen.
    # Normierung erfolgt auch Basis des Datenabschnitts, nicht den Gesamtzeitraum
    # Normierung auf 0 mit Standardabweichung 1
    df = df.copy()
    new_volume = df.volume - df.volume.mean()
    new_volume /= new_volume.std()
    df['volume'] = new_volume
    return df


def get_stock_prices_normalized(df, normalize_option):
    new_open = normalize_stock_price(df.open, normalize_option)
    new_close = normalize_stock_price(df.close, normalize_option)
    mean = (new_open.mean() + new_close.mean()) / 2
    std = (new_open.std() + new_close.std()) / 2
    # open
    df['open'] = (new_open - mean) / std
    # close
    df['close'] = (new_close - mean) / std
    return df
