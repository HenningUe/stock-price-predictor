# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def plot_history_dict(history_obj):
    metric_names = history_obj.model.metrics_names
    metric_names.remove('loss')
    acc_metric_name = metric_names[0]

    acc = history_obj.history[acc_metric_name]
    validate_acc = history_obj.history['val_' + acc_metric_name]

    loss = history_obj.history['loss']
    validate_loss = history_obj.history['val_loss']

    epochs = range(1, len(history_obj.epoch) + 1)

    # accuracy
    plt.plot(epochs, acc, color='red', marker='.', label='Training accuracy', linewidth=1)
    plt.plot(epochs, validate_acc, color='red', label='Validation accuracy', linewidth=1)

    # losses
    plt.plot(epochs, loss, color='green', marker='.', label='Training loss', linewidth=1)
    plt.plot(epochs, validate_loss, color='green', label='Validation loss', linewidth=1)
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()
