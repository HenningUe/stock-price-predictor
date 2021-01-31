
import numpy as np


def test_predict(model, x_test, y_test):
    test_predict = model.predict(x_test)
    test_is_real = y_test
    # combine to vectors to matrix (> [1, 2, 3] and [11, 12, 13] to [[1, 2, 3], [11, 12, 13]]
    test_predict_real_combined_as_mtx = np.column_stack([test_predict, test_is_real])

    # evaluate positive-predictions
    rtn_for_positives = \
        _get_number_of_prediction_matches_of_top_scores(test_predict_real_combined_as_mtx,
                                                        must_be_prediction=1)

    # evaluate negative-predictions
    rtn_for_negatives = \
        _get_number_of_prediction_matches_of_top_scores(test_predict_real_combined_as_mtx,
                                                        must_be_prediction=0)

    rate_of_elems_matching_vs_all_relevant_real_elems = \
        (rtn_for_positives['rate_of_elems_matching_vs_all_relevant_real_elems']
         +rtn_for_negatives['rate_of_elems_matching_vs_all_relevant_real_elems']) / 2.0  # @IgnorePep8

    rtn_dict = \
        dict(reference_value=rate_of_elems_matching_vs_all_relevant_real_elems,
             rate_of_elems_matching_vs_all_relevant_real_elems=rate_of_elems_matching_vs_all_relevant_real_elems,

             rate_of_elems_matching_vs_all_relevant_real_elems_for_positives=  # @IgnorePep8
                rtn_for_positives['rate_of_elems_matching_vs_all_relevant_real_elems'],  # @IgnorePep8
             usable_prediction_rate_for_positives=rtn_for_positives['usable_prediction_rate'],
             number_of_test_elements_matching_for_positives=rtn_for_positives['number_of_test_elements_matching'],
             total_elements_checked_for_positives=rtn_for_positives['total_elements_checked'],

             rate_of_elems_matching_vs_all_relevant_real_elems_for_negatives=  # @IgnorePep8
                rtn_for_negatives['rate_of_elems_matching_vs_all_relevant_real_elems'],  # @IgnorePep8
             usable_prediction_rate_for_negatives=rtn_for_negatives['usable_prediction_rate'],
             number_of_test_elements_matching_for_negatives=rtn_for_negatives['number_of_test_elements_matching'],
             total_elements_checked_for_negatives=rtn_for_negatives['total_elements_checked'],
             )

    return rtn_dict


def _get_number_of_prediction_matches_of_top_scores(test_predict_real_combined_as_mtx,
                                                    must_be_prediction):
    assert(must_be_prediction in [0, 1])

    total_real_elems_acc_to_must_be_prediction = \
        _get_matching_item_count_of_real_values(test_predict_real_combined_as_mtx, must_be_prediction)

    sort_direction = 'descending' if must_be_prediction == 1 else 'ascending'
    test_predict_real_combined_as_mtx_sorted_by_predict = \
        _sort_matrix(test_predict_real_combined_as_mtx, sort_direction)
    test_predict_real_combined_as_mtx_sorted_by_predict = \
        test_predict_real_combined_as_mtx_sorted_by_predict[:total_real_elems_acc_to_must_be_prediction]

    MIN_RATE_OF_MATCHING_PREDICTIONS_ON_TEST_DATA = 0.65  # = 65%
    prediction_match_count = 0
    elems_checked_count = 0
    for i in range(len(test_predict_real_combined_as_mtx_sorted_by_predict)):
        predict_val = test_predict_real_combined_as_mtx_sorted_by_predict[i][1]
        prediction_match_count += int(predict_val == must_be_prediction)
        elems_checked_count = i + 1
        match_rate = prediction_match_count / elems_checked_count
        if match_rate < MIN_RATE_OF_MATCHING_PREDICTIONS_ON_TEST_DATA:
            break
    number_of_test_elements_matching = prediction_match_count
    usable_prediction_rate = None
    total_elements_checked = elems_checked_count
    total_match_rate_for_testet_elems = 0.0
    rate_of_elems_matching_vs_all_relevant_real_elems = 0.0
    if prediction_match_count > 0:
        total_match_rate_for_testet_elems = number_of_test_elements_matching / total_elements_checked
    if number_of_test_elements_matching > 0 \
       and total_match_rate_for_testet_elems >= MIN_RATE_OF_MATCHING_PREDICTIONS_ON_TEST_DATA:
        rate_of_elems_matching_vs_all_relevant_real_elems = \
            float(number_of_test_elements_matching / total_real_elems_acc_to_must_be_prediction)
        usable_prediction_rate = float(test_predict_real_combined_as_mtx_sorted_by_predict[i - 1][0])
    return dict(rate_of_elems_matching_vs_all_relevant_real_elems=rate_of_elems_matching_vs_all_relevant_real_elems,
                usable_prediction_rate=usable_prediction_rate,
                number_of_test_elements_matching=int(number_of_test_elements_matching),
                total_elements_checked=int(total_elements_checked))


def _get_matching_item_count_of_real_values(test_predict_real_combined_as_mtx, must_be_prediction,
                                            column_containing_real_vals=1):
    vect = test_predict_real_combined_as_mtx[:, column_containing_real_vals]
    count = len(vect[vect == must_be_prediction])
    return count


def _sort_matrix(matrix_in, sort_direction, column_used_for_sorting=0):
    sort_direction = sort_direction.lower()
    assert(sort_direction in ['ascending', 'descending'])
    # sort by first column, test_predict > sort direction lowest to highest
    matrix_in = matrix_in[matrix_in[:, column_used_for_sorting].argsort()]
    if sort_direction == 'descending':
        # flip sort direction highest tp lowest
        matrix_in = np.flipud(matrix_in)
    return matrix_in
