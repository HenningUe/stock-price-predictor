
import numpy as np


def test_predict(model, x_test, y_test):
    test_predict = model.predict(x_test)
    test_is_real = y_test
    test_predict_real_combined = np.column_stack([test_predict, test_is_real])
    test_predict_real_combined_sorted = test_predict_real_combined[test_predict_real_combined[:, 0].argsort()]
    test_predict_real_combined_sorted = np.flipud(test_predict_real_combined_sorted)
    pos_count = 0
    MIN_RATE_OF_MATCHING_PREDICTIONS_ON_TEST_DATA = 0.85
    for i in range(len(test_predict_real_combined_sorted)):
        pos_count += test_predict_real_combined_sorted[i][1]
        if i >= 1 and pos_count / (i + 1) < MIN_RATE_OF_MATCHING_PREDICTIONS_ON_TEST_DATA:
            break
    number_of_test_elements_matching = pos_count
    total_elements_checked = i
    usable_rate = None
    if number_of_test_elements_matching > 0 \
       and pos_count / total_elements_checked >= MIN_RATE_OF_MATCHING_PREDICTIONS_ON_TEST_DATA:
        usable_rate = test_predict_real_combined_sorted[i - 1][0]
    return dict(usable_rate=usable_rate,
                number_of_test_elements_matching=number_of_test_elements_matching,
                total_elements_checked=total_elements_checked)
