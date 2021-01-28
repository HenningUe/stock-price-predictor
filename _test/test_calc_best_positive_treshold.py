
import pandas as pd

import _init  # @UnresolvedImport @UnusedImport

import write_read


def get_treshold_positive():
    df_quantile_dists = _get_treshold()

    # Ergebnis Treshold
    # +0,8% (18 % aller Faelle = 243 in 10 J = 24 / J)
    # oder
    # +1% (11 % aller Faelle = 146 in 10 J = 15 / J)
    # oder
    # +2% (1,8 % aller Faelle = 24 in 10 J = 2,4 / J)
    x = 1


def get_treshold_negative():
    df_quantile_dists = _get_treshold()

    # Ergebnis Treshold
    # +0,8% (18 % aller Faelle = 243 in 10 J = 24 / J)
    # oder
    # +1% (11 % aller Faelle = 146 in 10 J = 15 / J)
    # oder
    # +2% (1,8 % aller Faelle = 24 in 10 J = 2,4 / J)
    x = 1


def _get_treshold(neg_factor=1):
    df = write_read.all_in_one.get_yahoo_daydeltas_from_date_range_as_dframe(symbol="SPY")
    df_pos = df[df.day_delta > 0]
    STEP_DIST = 0.001

    df_quantile_dists = pd.DataFrame(columns=['quantile_pos', 'val_count'])
    quantile_pos = 0
    while True:
        df_tmp = df_pos[(quantile_pos < df_pos.day_delta) & (df_pos.day_delta <= quantile_pos + STEP_DIST)]

        if quantile_pos + STEP_DIST >= df_pos.day_delta.max():
            break
        df_quantile_dists = \
            df_quantile_dists.append(dict(quantile_pos=quantile_pos, val_count=len(df_tmp)), ignore_index=True)
        quantile_pos += STEP_DIST
    df_quantile_dists.index = df_quantile_dists.quantile_pos

    # Ergebnis Treshold
    # +0,8% (18 % aller Faelle = 243 in 10 J = 24 / J)
    # oder
    # +1% (11 % aller Faelle = 146 in 10 J = 15 / J)
    # oder
    # +2% (1,8 % aller Faelle = 24 in 10 J = 2,4 / J)
    x = 1


get_treshold()
