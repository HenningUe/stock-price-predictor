
import keras

from _misc_frogs import loggermod


class EarlyStoppingCustom(keras.callbacks.Callback):

    def __init__(self,
                 complete_test_data,
                 test_predict_func,
                 patience=5,
                 restore_best_weights=True):
        super().__init__()
        self.complete_test_data = complete_test_data
        self.test_predict_func = test_predict_func
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
        result = self.test_predict_func(self.model, self.complete_test_data['x'], self.complete_test_data['y'])
        result['epoch'] = epoch
        if self.best_guess is None \
           or (result['reference_value'] > self.best_guess['reference_value']):
            self.best_guess = result
            self.best_weights = self.model.get_weights()
            self.wait = 0
        else:
            self.wait += 1
            if self.wait > self.patience:
                self._logger.info('Interrupting model training since metric has not improved for '
                                  'last {} epochs.'.format(self.patience))
                self.stopped_epoch = epoch
                self.model.stop_training = True
                if self.restore_best_weights and self.best_weights is not None:
                    self._logger.info('Restoring model weights from the end of the best epoch.')
                    self.model.set_weights(self.best_weights)
            self.guesses.append(result)

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            self._logger.info('Epoch {}: early stopping.'.format(self.stopped_epoch + 1))
            self._logger.info('Reference metric''s value: {}.'
                              .format(self.best_guess['reference_value']))
