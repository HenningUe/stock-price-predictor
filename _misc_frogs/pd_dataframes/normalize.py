
import datetime as dt
import pandas as pd
# import numpy as np


def normalize_column(col_in, mean_std_spec=None):
    if mean_std_spec is None:
        mean = col_in.mean()
        std = col_in.std()
    else:
        mean = mean_std_spec['mean']
        std = mean_std_spec['std']
    col_norm = (col_in - mean) / std
    return col_norm


def normalize_stock_price(stock_price_vector, normalize_option='relative_to_first_batch_price'):
    if normalize_option.lower() == "relative_to_previous_data_point":
        return normalize_stock_price_option_a_relative_to_previous_data_point(stock_price_vector)
    elif normalize_option.lower() == "relative_to_first_batch_price":
        return normalize_stock_price_option_b_relative_to_first_batch_price(stock_price_vector)
    elif normalize_option.lower() == "relative_to_day_mean(":
        return normalize_stock_price_option_c_relative_to_day_mean(stock_price_vector)
    else:
        raise NotImplementedError()


def normalize_stock_price_option_a_relative_to_previous_data_point(stock_price_vector):
    # IDEE:
    # Option A)
    # Ideal waere es, den relativen Anstieg von Datenpunkt zu Datenpunkt zu machen. Das Problem ist, dass
    # die zeitl. Abstaende zwischen den Datenpunkten nicht immer identisch sind. Zudem sind die zeitl. Abstaende
    # zwischen den Datenpunkten der firstratedata-Daten andere (naemlich beliebige Abstaende), als die, die man
    # z.B. von Yahoo erhaelt (naemlich immer 5 Minuten).
    raise NotImplementedError()


def normalize_stock_price_option_b_relative_to_first_batch_price(stock_price_vector):
    # IDEE:
    # Option B)
    # Relative Entwicklung bezogen bezogen auf 1ten verfuegbaren Kurs. Problematisch, da mit
    # groesserem  Abstand zum ersten Punkt auch die Ausschlaege groesser werden > Macht die Normierung auf 1 schwierig
    # ABER Vorteil: Es bleibt die die Information erhalten, wie sich die Kurse innerhalb eines Batches entwickelten
    first_valid_val = stock_price_vector[stock_price_vector.first_valid_index()]
    price_rel = stock_price_vector / first_valid_val
    return price_rel


def normalize_stock_price_option_c_relative_to_day_mean(stock_price_vector):
    # IDEE:
    # Option C)
    # Relative Entwicklung bezogen auf den Durchschnitt eines Tages. Vorteil: Gilt fuer beliege Anzahl Tage, d.h.
    # frei skalierbar. Sollte die Kursverlaeufe sinnvoll repraesentieren.
    #  > Im ersten Schritt fuer alle Tage die Durchschnitte ausrechnen
    #  > Dann fuer jeden Kurs die relative Abweichung auf seinen Tagesdurchschnitt bezogen

    df_price = pd.DataFrame(index=stock_price_vector.index)
    df_price['price'] = stock_price_vector
    df_mean = df_price.groupby([df_price.index.year, df_price.index.month, df_price.index.day]).agg(dict(price='mean'))
    df_mean.rename(columns={'price': 'price_mean_per_day'}, inplace=True)

    _get_date = lambda val_in: dt.date(*val_in)  # @IgnorePep8
    df_mean['day'] = df_mean.index.map(_get_date)
    # https://stackoverflow.com/questions/27080542/merging-combining-two-dataframes-with-different-frequency-time-series-indexes-in
    df_price['day'] = df_price.index.date
    df_mean.index = df_mean.day
    df = df_price.join(df_mean, on='day', how='left', rsuffix='_1')
    df = df.drop(['day'], axis=1)
    df = df.drop(['day_1'], axis=1)
    df.loc[df['price'] == 0, 'price_mean_per_day'] = 0
    price_rel = df['price'] / df['price_mean_per_day'] - 1
    return price_rel
