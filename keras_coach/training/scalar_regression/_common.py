

def extract_np_labels_from_df_raw(df_labels):
    df_labels['rel_increate'] = (df_labels.close - df_labels.open) / df_labels.open
    np_labels = df_labels.rel_increate.to_numpy()
    return np_labels


def get_class_weights(y_train):
    return None
