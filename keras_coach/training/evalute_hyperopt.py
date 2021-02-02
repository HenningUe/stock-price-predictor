# -*- coding: utf-8 -*-

import keras_coach.training
from keras_coach.training._all import swish, model_store, traindata


def evaluate_best_models_by_test_data_all():
    funcs = []
    for func in funcs:
        evaluate_best_models_by_test_data_single_func(func)


def evaluate_best_models_by_test_data_single_func(func_name):
    mdls = model_store.get_models_sorted_by_reference_value(func_name)
    # : :type best_mdl: model_store.ModelBin
    best_mdl = mdls[0]
    train_mod = getattr(keras_coach.training, 'mod_name')

    swish.register_swish_activation_func()
    print("Get training data")
    x_train_data, y_label_df_raw = traindata.get_training_data(best_mdl.length_in_days)
    y_label_data = train_mod.extract_np_labels_from_df_raw(y_label_df_raw)

    print("Build and fit model")
    # Split the data up in train and test sets
    data = traindata.split_data(x_train_data, y_label_data)
    best_mdl.load_model()
    result = best_mdl.model.predict(data['x_test'])
