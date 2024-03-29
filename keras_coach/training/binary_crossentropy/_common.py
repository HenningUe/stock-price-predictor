
import numpy as np
from sklearn.utils import class_weight


def extract_np_labels_from_df_raw(df_labels):
    df_labels['direction_flag'] = df_labels.close > df_labels.open
    np_labels = df_labels.direction_flag.astype(int).to_numpy()
    return np_labels


def get_class_weights(y_train):
    class_weights = \
        class_weight.compute_class_weight(class_weight='balanced', classes=np.unique(y_train), y=y_train)
    class_weights = {0: class_weights[0], 1: class_weights[1]}
    return class_weights
