
import tensorflow as tf
from keras import models, layers, optimizers, metrics, regularizers, losses  # @UnusedImport

from keras_coach.training._all import colab_hw, debug


def finish_and_compile_mdl(model):
    model.add(layers.Dense(1, activation='sigmoid'))
    if debug.HYPEROPT_SIMULATE:
        model = None

    elif not colab_hw.is_to_be_run_on_tpu():
        opt = optimizers.RMSprop(lr=0.001)
        model.compile(optimizer=opt,
                      loss=losses.binary_crossentropy,
                      metrics=['accuracy'])

    elif colab_hw.is_to_be_run_on_tpu():
        tpu_address = colab_hw.get_tpu_address()
        resolver = tf.distribute.cluster_resolver.TPUClusterResolver(tpu_address)
        tf.config.experimental_connect_to_cluster(resolver)
        tf.tpu.experimental.initialize_tpu_system(resolver)
        strategy = tf.distribute.experimental.TPUStrategy(resolver)
        with strategy.scope():
            opt = tf.optimizers.RMSprop(learning_rate=0.001)
            model.compile(optimizer=opt,
                          loss=tf.keras.losses.binary_crossentropy,
                          metrics=['accuracy'])

    return model
