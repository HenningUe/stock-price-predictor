# -*- coding: utf-8 -*-

import tensorflow as tf

from _misc_frogs import environment
from . import debug


class MultiGPUMdlBuilder(object):

    def __init__(self):
        self.strategy = None
        if not debug.HYPEROPT_SIMULATE and environment.get_runtime_env() == "aws1":
            self.strategy = tf.distribute.MirroredStrategy()

    def number_of_gpus(self):
        if self.strategy is None:
            return 0
        else:
            return self.strategy.num_replicas_in_sync

    def __enter__(self, *args, **kwargs):
        if self.strategy is not None:
            self.strategy.__enter__(*args, **kwargs)
        return self.strategy

    def __exit__(self, *args, **kwargs):
        if self.strategy is not None:
            self.strategy.__exit__(*args, **kwargs)


multi_gpu_mdl_builder = MultiGPUMdlBuilder()
