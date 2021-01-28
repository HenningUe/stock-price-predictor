
import keras

from ._predict_test import test_predict

_best_guess = list()
_best_weights = list()


def get_test_prediction_results():
    global _best_guess, _best_weights
    return _best_guess, _best_weights


class EarlyStoppingCustom(keras.callbacks.Callback):
    """Stop training when the loss is at its min, i.e. the loss stops decreasing.

  Arguments:
      patience: Number of epochs to wait after min has been hit. After this
      number of no improvement, training stops.
  """

    def __init__(self, test_x, test_y):
        super().__init__()
        self.test_x = test_x
        self.test_y = test_y
        self.best_guess = list()
        self.best_weights = list()

    def on_train_begin(self, logs=None):
        self.best_guess = list()

    def on_epoch_end(self, epoch, logs=None):
        # current = logs.get("loss")
        result = test_predict(self.model, self.test_x, self.test_y)
        if result['usable_rate'] is not None:
            store_result = True
#             if self.best_guess is None:
#                 store_result = True
#             elif self.best_guess['number_of_test_elements_matching'] < result['number_of_test_elements_matching']:
#                 store_result = True  # @NOSONAR
#             elif (self.best_guess['number_of_test_elements_matching'] == result['number_of_test_elements_matching']
#                   and self.best_guess['usable_rate'] < result['usable_rate']):
#                 store_result = True  # @NOSONAR
            if store_result:
                result['epoch'] = epoch
                self.best_guess.append(result)
                self.best_weights.append(self.model.get_weights())

    def on_train_end(self, logs=None):
        global _best_guess, _best_weights
        if self.best_guess is not None:
            _best_guess = self.best_guess
            _best_weights = self.best_weights
