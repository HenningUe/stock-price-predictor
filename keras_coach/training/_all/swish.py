# -*- coding: utf-8 -*-

from keras.backend import sigmoid
from keras import layers

from tensorflow.python.keras import utils

from keras_coach.training._all import model_store


def register_swish_activation_func():
    # https://www.bignerdranch.com/blog/implementing-swish-activation-function-in-keras/

    def _swish(x, beta=1):
        return (x * sigmoid(beta * x))

    utils.generic_utils.get_custom_objects().update({'swish': layers.Activation(_swish)})


def insert_swish_in_mdl_struct_files(environment=None):
    mdl_bins = model_store.get_models(environment)
    print("Number files {}".format(len(mdl_bins)))
    for mdl_bin in mdl_bins:
        mdl_struc_file = mdl_bin.get_filep_model_structure()
        print("Modifing: {}".format(str(mdl_struc_file)))
        _insert_swish_in_mdl_struct_file(mdl_struc_file)


def _insert_swish_in_mdl_struct_file(mdl_struc_file):
    REPLACE_DEFS = [dict(old="class_name: Activation", new="class_name: swish"),
                    dict(old="activation: _swish", new="activation: swish"),
                    ]
    with mdl_struc_file.open('r') as f:
        content = f.read()
    for rdef in REPLACE_DEFS:
        content = content.replace(rdef['old'], rdef['new'])
    with mdl_struc_file.open('w') as f:
        f.write(content)


if __name__ == "__main__":
    insert_swish_in_mdl_struct_files()
