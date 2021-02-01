
import numpy as np
import sklearn.metrics


def test_predict(model, x_test, y_test):
    test_predict = model.predict(x_test)
    test_predict = test_predict.reshape(test_predict.shape[0] * test_predict.shape[1])
    test_is_real = y_test
    number_of_positive_labels = np.count_nonzero(test_is_real[test_is_real >= 0])
    number_of_negative_labels = np.count_nonzero(test_is_real[test_is_real < 0])

    vector_of_direction_matches = (test_is_real >= 0) == (test_predict >= 0)
    number_of_matches = np.count_nonzero(vector_of_direction_matches)
    if len(vector_of_direction_matches) == 0:
        ratio_total = 0
    else:
        ratio_total = number_of_matches / len(vector_of_direction_matches)

    vector_positive_predicts = test_predict >= 0
    test_is_real_positive = test_is_real >= 0
    test_predict_only_positives = test_predict[vector_positive_predicts]
    precision_positive = sklearn.metrics.precision_score(test_is_real_positive, vector_positive_predicts)
    test_is_real_only_positives_acc_to_predict = test_is_real[vector_positive_predicts]
    vector_of_direction_matches = \
        (test_is_real_only_positives_acc_to_predict >= 0) == (test_predict_only_positives >= 0)
    number_of_matches = np.count_nonzero(vector_of_direction_matches)
    if len(vector_of_direction_matches) == 0:
        ratio_only_positives = 0
    else:
        ratio_only_positives = number_of_matches / len(vector_of_direction_matches)

    vector_negative_predicts = ~vector_positive_predicts
    test_is_real_negative = test_is_real < 0
    precision_negative = sklearn.metrics.precision_score(test_is_real_negative, vector_negative_predicts)
    test_predict_only_negatives = test_predict[vector_negative_predicts]
    test_is_real_only_negatives_acc_to_predict = test_is_real[vector_negative_predicts]
    vector_of_direction_matches = \
        (test_is_real_only_negatives_acc_to_predict < 0) == (test_predict_only_negatives < 0)
    number_of_matches = np.count_nonzero(vector_of_direction_matches)
    if len(vector_of_direction_matches) == 0:
        ratio_only_negatives = 0
    else:
        ratio_only_negatives = number_of_matches / len(vector_of_direction_matches)

    if ratio_only_positives == 0 or ratio_only_negatives == 0:
        precision_total = 0
    else:
        precision_total = (precision_positive + precision_negative) / 2

    return dict(reference_value=float(precision_total),
                ratio_total=float(ratio_total),
                precision_positives=float(precision_positive),
                ratio_only_positives=float(ratio_only_positives),
                precision_negatives=float(precision_negative),
                ratio_only_negatives=float(ratio_only_negatives),
                precision_total=float(precision_total),
                number_of_positive_labels=int(number_of_positive_labels),
                number_of_negative_labels=int(number_of_negative_labels),
                )
