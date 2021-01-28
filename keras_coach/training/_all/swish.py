# -*- coding: utf-8 -*-

from keras.backend import sigmoid
from keras import layers

from tensorflow.python.keras import utils

# hhttps://www.bignerdranch.com/blog/implementing-swish-activation-function-in-keras/


def register_swish_activation_func():

    def _swish(x, beta=1):
        return (x * sigmoid(beta * x))

    utils.generic_utils.get_custom_objects().update({'swish': layers.Activation(_swish)})
