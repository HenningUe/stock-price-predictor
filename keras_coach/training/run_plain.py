# -*- coding: utf-8 -*-

from pprint import pprint

from keras_coach.training._all import swish, plot, model_store, traindata

# https://github.com/fchollet/deep-learning-with-python-notebooks/blob/master/3.6-classifying-newswires.ipynb

# naechste Schritte:
# https://medium.com/analytics-vidhya/what-nobody-tells-you-about-binary-classification-metrics-4998574b668
# ... accuracy is not a good meatric


def _get_train_module():
    from keras_coach.training import scalar_regression, binary_crossentropy  # @UnusedImport
    if 1:
        return binary_crossentropy
    else:
        return scalar_regression


def main():
    swish.register_swish_activation_func()
    train_mod = _get_train_module()
    print("Get training data")
    training_data_length_in_days = 5
    x_train_data, y_label_df_raw = traindata.get_training_data(training_data_length_in_days)
    y_label_data = train_mod.extract_np_labels_from_df_raw(y_label_df_raw)

    print("Build and fit model")
    # Split the data up in train and test sets
    data = traindata.split_data(x_train_data, y_label_data)

    build_f = 0
    if build_f == 0:
        build_model_func = train_mod.BuildMdlFuncs.build_model_dense_pure
    elif build_f == 1:
        build_model_func = train_mod.BuildMdlFuncs.build_model_cnn
    elif build_f == 2:
        build_model_func = train_mod.BuildMdlFuncs.build_model_recurrent_lstm
    elif build_f == 3:
        build_model_func = train_mod.BuildMdlFuncs.build_model_recurrent_lstm_with_cnn

    model = build_model_func(data['x_train'])
    callb = train_mod.EarlyStoppingCustom(dict(x=data['x_validate'], y=data['y_validate']))
    class_weight = train_mod.get_class_weights(data['y_train'])
    MAX_EPOCHS = 1
    history = model.fit(data['x_train'], data['y_train'],
                        epochs=MAX_EPOCHS,
                        validation_data=(data['x_validate'], data['y_validate']),
                        callbacks=[callb], class_weight=class_weight)

    if callb.best_guess is not None:
        params = dict(train_module=train_mod.__name__.split('.')[-1],
                      model_build_func=build_model_func.__name__,
                      epoch=callb.best_guess['epoch'],
                      length_in_days=training_data_length_in_days,
                      reference_value=float(callb.best_guess['reference_value']))
        model_store.save_model(model, params, callb.best_guess)
    pprint(callb.guesses)

    print("Plot results")
    plot.plot_history_dict(history)
    print("Finished")


main()
