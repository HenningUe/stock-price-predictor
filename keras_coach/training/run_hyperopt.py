# -*- coding: utf-8 -*-

from pprint import pprint  # @UnusedImport

import hyperopt as hypopt

from _misc_frogs import loggermod, environment
from keras_coach.training._all import debug, hyperopt_store, swish, misc, colab_hw
from keras_coach.training._all import hyperopt_monkeyp  # @UnusedImport
from keras_coach.training._all.models_hyperopt import obj_func_wrapper, space_and_mdl_templates

MAX_EVALUATIONS = 130 if environment.runs_in_colab() else 20
RUN_MDL_FUNCS_INDIVIDUAL = True
debug.HYPEROPT_SIMULATE = False


def main(func_name=None):
    swish.register_swish_activation_func()
    train_modules = _get_train_modules()
    for train_mod in train_modules:
        run_single_module(train_mod, func_name)
    # hypopt.progress.default_callback(initial, total)
    # Save and reload evaluations > https://github.com/hyperopt/hyperopt/issues/267

# rnn_lstm_pure


def run_single_module(train_mod, func_name=None):
    global RUN_MDL_FUNCS_INDIVIDUAL, MAX_EVALUATIONS
    loggermod.init_logger(misc.get_modul_name_pure(train_mod) + "__hyperopt")
    logger = loggermod.get_logger()
    logger.info("Start hyperopt")
    logger.info("Train module: {}".format(misc.get_modul_name_pure(train_mod)))
    logger.info("Is 'HYPEROPT_SIMULATE': {}".format(debug.HYPEROPT_SIMULATE))
    logger.info("Is 'RUN_MDL_FUNCS_INDIVIDUAL': {}".format(RUN_MDL_FUNCS_INDIVIDUAL))
    logger.info("'MAX_EVALUATIONS': {}".format(MAX_EVALUATIONS))
    logger.info("User colab hardware: {}".format(colab_hw.get_hw_support_type()))
    space = space_and_mdl_templates.get_hyperopt_space(get_functions_individual=RUN_MDL_FUNCS_INDIVIDUAL)
    for func_space in space:
        if RUN_MDL_FUNCS_INDIVIDUAL:
            if func_name is not None and not func_name.lower() == func_space['funcname'].lower():
                continue
            logger.info("Running hyperopt space for func: {}".format(func_space['funcname']))
        _run_single_scenario(train_mod, func_space)


def _run_single_scenario(train_mod, space):
    global MAX_EVALUATIONS
    logger = loggermod.get_logger()
    max_evals = MAX_EVALUATIONS
    if debug.HYPEROPT_SIMULATE:
        max_evals = 20
    f_nn = obj_func_wrapper.get_objective_func_wrapped(train_mod)
    algo_func = hypopt.tpe.suggest
    trials = hypopt.Trials()
    best_trial = hypopt.fmin(f_nn, space, algo=algo_func, max_evals=max_evals,
                             trials=trials, verbose=True)

    params = dict(train_module=misc.get_modul_name_pure(train_mod), max_evals=max_evals,
                  algo_func=".".join([algo_func.__module__, algo_func.__name__]))
    hyperopt_store.save_hyperopt_trial(params, best_trial, trials)

    logger.info('best_trial: ', best_trial)
    logger.info("Finished")


def _get_train_modules():
    from keras_coach.training import scalar_regression, binary_crossentropy  # @UnusedImport
    x = 1
    if x == 0:
        return [scalar_regression, binary_crossentropy]
    elif x == 1:
        return [scalar_regression]
    elif x == 2:
        return [binary_crossentropy]


if __name__ == "__main__":
    main()
