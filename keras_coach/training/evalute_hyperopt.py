# -*- coding: utf-8 -*-

import keras_coach.training
from keras_coach.training._all import swish, model_store, traindata


def evaluate_best_models_by_test_data_all():
    funcs = ['dense_pure', 'rnn_lstm_pure']
    for func in funcs:
        print("===========================")
        print(func)
        evaluate_best_models_by_test_data_single_func(func)


def evaluate_best_models_by_test_data_single_func(func_name):
    mdl_bins = model_store.get_models_sorted_by_reference_value(func_name, 'localcolab')
    # : :type best_mdl_bin: model_store.ModelBin
    max_bins = 3 if len(mdl_bins) >= 3 else len(mdl_bins)
    for best_mdl_bin in mdl_bins[:max_bins]:
        train_mod = getattr(keras_coach.training, best_mdl_bin.train_module)

        swish.register_swish_activation_func()
        print("---------------")
        print("Get training data")
        x_train_data, y_label_df_raw = traindata.get_training_data(best_mdl_bin.length_in_days)
        y_label_data = train_mod.extract_np_labels_from_df_raw(y_label_df_raw)

        print("Make prediction")
        # Split the data up in train and test sets
        data = traindata.split_data(x_train_data, y_label_data)
        best_mdl_bin.load_model()
        result = train_mod.test_predict(best_mdl_bin.model, data['x_test'], data['y_test'])
        print(best_mdl_bin.ref_val)
        print(result['reference_value'])
        print(best_mdl_bin.model.summary())


if __name__ == "__main__":
    evaluate_best_models_by_test_data_all()
