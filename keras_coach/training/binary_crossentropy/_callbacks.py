
import keras

from _misc_frogs import loggermod
from ._predict_test import test_predict


class EarlyStoppingCustom(keras.callbacks.Callback):

    def __init__(self,
                 complete_test_data,
                 patience=4,
                 restore_best_weights=True):
        super().__init__()
        self.complete_test_data = complete_test_data
        self.patience = patience
        self.wait = 0
        self.stopped_epoch = 0
        self.restore_best_weights = restore_best_weights
        self.guesses = list()
        self.best_guess = None
        self.best_weights = None
        self._logger = loggermod.get_logger()

    def on_train_begin(self, logs=None):
        # Allow instances to be re-used
        self.wait = 0
        self.stopped_epoch = 0
        self.best_weights = None

    def on_epoch_end(self, epoch, logs=None):
        # current = logs.get("loss")
        result = test_predict(self.model, self.complete_test_data['x'], self.complete_test_data['y'])
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
