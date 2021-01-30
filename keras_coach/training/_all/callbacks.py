
import keras

from _misc_frogs import loggermod


class EarlyStoppingCustom(keras.callbacks.Callback):

    def __init__(self,
                 complete_test_data,
                 patience=5,
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

    def on_epoch_end(self, epoch, logs=None):  # @NOSONAR
        raise NotImplementedError("In super class")

    def on_train_end(self, logs=None):
        if self.stopped_epoch > 0:
            self._logger.info('Epoch {}: early stopping.'.format(self.stopped_epoch + 1))
