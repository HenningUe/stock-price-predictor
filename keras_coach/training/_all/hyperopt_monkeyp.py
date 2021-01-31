
from hyperopt import hp
from hyperopt.pyll import scope


def _hp_uniformint(label, *args, **kwargs):
    kwargs["q"] = 1.0
    return scope.int(hp.quniform(label, *args, **kwargs))


def _monkey_patch_hyperopt():
    if 'uniformint' not in dir(hp):
        hp.uniformint = _hp_uniformint


_monkey_patch_hyperopt()
