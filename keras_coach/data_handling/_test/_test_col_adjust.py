import pandas as pd

import keras_coach.data_handling.normalize._pframe_cols_adjust as dataprep


def test_get_normalize_stock_price():
    matrix = [(222, 34),
              (230, 31),
              (228, 38),
              (237, 40),
              (239, 33),
              (241, 35)
              ]
    dataframe = pd.DataFrame(matrix, columns=list('close', 'open'))
    dataframe = dataprep.get_stock_prices_normalized(dataframe)
    print(dataframe)


def test_get_max_min_diff():
    matrix = [(30, 34),
              (31, 37),
              (30, 31),
              (33, 36),
              (40, 50),
              (21, 35)
              ]
    dataframe = pd.DataFrame(matrix, columns=list('min', 'max'))
    dataframe = dataprep.get_max_min_diff_normalized(dataframe)
    print(dataframe)


def test_get_volume_normalized():
    matrix = [(30,),
              (31,),
              (30,),
              (33,),
              (40,),
              (21,)
              ]
    dataframe = pd.DataFrame(matrix, columns=list(['volume', ]))
    dataframe = dataprep.get_volume_normalized(dataframe)
    print(dataframe)


if __name__ == "__main__":
    test_get_volume_normalized()
    test_get_normalize_stock_price()
    test_get_max_min_diff()
