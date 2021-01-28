
import datetime
import numpy as np

from keras_coach import data_handling


def test_numpy():
    # size = 2 x 4 x 3
    first = np.array([
                        [[1111, 1112, 1113], [1121, 1122, 1123], [1131, 1132, 1133], [1141, 1142, 1143], ],
                        [[1211, 1212, 1213], [1221, 1222, 1223], [1231, 1232, 1233], [1241, 1242, 1243], ],
                     ])

    secon = np.array([
                        [[2111, 2112, ], [2121, 2122, ], [2131, 1132, ], [2141, 2142, ], ],
                        [[2211, 2212, ], [2221, 2222, ], [2231, 2232, ], [2241, 2242, ], ],
                     ])

    c = np.concatenate([first, secon], axis=2)
    x = 1


def test_train_data():
    data_handling.get_np_data_sets(["ES=F", "SPY"], datetime.timedelta(days=2))


if __name__ == "__main__":
    # test_numpy()
    test_train_data()
