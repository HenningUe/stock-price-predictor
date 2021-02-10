# -*- coding: utf-8 -*-

import pprint

import keras_coach.training
from keras_coach.training._all import swish, model_store, traindata, hyperopt_store


def evaluate_best_models_by_test_data_all():
    funcs = ['dense_pure', 'cnn_pure', 'rnn_lstm_pure', 'rnn_lstm_with_cnn']
    funcs = ['dense_pure', 'rnn_lstm_with_cnn']
    good_mdl_ids = list()
    for func in funcs:
        print("===========================================================")
        print("================================")
        print("==========")
        print(func.upper())
        evaluate_best_models_by_test_data_single_func(func, good_mdl_ids)
    pprint.pprint(good_mdl_ids)
    hyperopt_store.save_hyper_hyperopt_models(good_mdl_ids)


def evaluate_best_models_by_test_data_single_func(func_name, good_mdls):
    mdl_bins = model_store.get_models_sorted_by_reference_value(func_name, 'local')
    # : :type best_mdl_bin: model_store.ModelBin
    MAX_MDLS_TEST = 4 if func_name == 'rnn_lstm_pure' else 33
    max_bins = MAX_MDLS_TEST if len(mdl_bins) >= MAX_MDLS_TEST else len(mdl_bins)

    for best_mdl_bin in mdl_bins[:max_bins]:
        train_mod = getattr(keras_coach.training, best_mdl_bin.train_module)

        swish.register_swish_activation_func()
        x_train_data, y_label_df_raw = traindata.get_training_data(best_mdl_bin.length_in_days)
        y_label_data = train_mod.extract_np_labels_from_df_raw(y_label_df_raw)

        # Split the data up in train and test sets
        data = traindata.split_data(x_train_data, y_label_data, hyper_test_percent=0.06)
        best_mdl_bin.load_model()
        result = train_mod.test_predict(best_mdl_bin.model, data['x_test'], data['y_test'])
        is_good = result['reference_value'] >= 0.65
        if is_good:
            print("---------------")
            print(best_mdl_bin.ref_val)
            print("Calculated ref: {}".format(result['reference_value']))
            # is_good_str = "IS GOOOOOD" if is_good else "--"
            # print(is_good_str)
            print(best_mdl_bin.length_in_days)
            good_mdls.append(best_mdl_bin.dir.name)
            # best_mdl_bin.model.summary()
        # print(xx[0])


if __name__ == "__main__":
    evaluate_best_models_by_test_data_all()
