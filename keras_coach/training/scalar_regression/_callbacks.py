
from .._all import callbacks
from ._predict_test import test_predict


class EarlyStoppingCustom(callbacks.EarlyStoppingCustom):

    def on_epoch_end(self, epoch, logs=None):
        result = test_predict(self.model, self.complete_test_data['x'], self.complete_test_data['y'])
        result['epoch'] = epoch
        if self.best_guess is None or result['precision_total'] > self.best_guess['precision_total']:
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
