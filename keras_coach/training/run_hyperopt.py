# -*- coding: utf-8 -*-

from pprint import pprint  # @UnusedImport

import pickle
import hyperopt as hypopt
import cloudpickle

from _misc_frogs import loggermod, environment
from keras_coach.training._all import debug, hyperopt_store, swish, misc, colab_hw
from keras_coach.training._all import hyperopt_monkeyp  # @UnusedImport
from keras_coach.training._all.models_hyperopt import obj_func_wrapper, space_and_mdl_templates

MAX_EVALUATIONS = 130 if environment.runs_in_colab() else 20
RUN_MDL_FUNCS_INDIVIDUAL = True
debug.HYPEROPT_SIMULATE = True


def m_patch():
    # monkey patch to replace fancy functions by original pickle ones
    cloudpickle.dump = pickle.dump
    cloudpickle.load = pickle.load


m_patch()


def main(func_name=None):
    swish.register_swish_activation_func()
    train_modules = _get_train_modules()
    for train_mod in train_modules:
        run_single_module(train_mod, func_name)
    # hypopt.progress.default_callback(initial, total)
    # Save and reload evaluations > https://github.com/hyperopt/hyperopt/issues/267

# rnn_lstm_pure


def run_single_module(train_mod, func_name_to_use=None, func_name_not_to_use=None):
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
    algo_func = hypopt.tpe.suggest
    for func_space in space:
        c_func_name = None
        if RUN_MDL_FUNCS_INDIVIDUAL:
            c_func_name = func_space['funcname']
            if func_name_not_to_use is not None and func_name_not_to_use.lower() == c_func_name.lower():
                continue
            if func_name_to_use is not None and not func_name_to_use.lower() == c_func_name.lower():
                continue
            logger.info("Running hyperopt space for func: {}".format(c_func_name))
        _run_single_scenario(train_mod, func_space, c_func_name, algo_func)

    # delete all trials objects after successful termination of all trials
    for func_space in space:
        c_func_name = None
        if RUN_MDL_FUNCS_INDIVIDUAL:
            c_func_name = func_space['funcname']
        params = _get_func_signature_params(train_mod, algo_func, c_func_name, MAX_EVALUATIONS)
        hyperopt_store.delete_hyperopt_trial(params)


def _run_single_scenario(train_mod, space, func_name, algo_func):
    global MAX_EVALUATIONS
    logger = loggermod.get_logger()
    max_evals = MAX_EVALUATIONS
    if debug.HYPEROPT_SIMULATE:
        max_evals = 10
    f_nn = obj_func_wrapper.get_objective_func_wrapped(train_mod)
    params = _get_func_signature_params(train_mod, algo_func, func_name, max_evals)
    trials = hyperopt_store.load_hyperopt_trial(params)
    if trials is not None and len(trials.tids) == max_evals:
        logger.info('Already went through in last run. Abortion.')
        return
    elif trials is not None and len(trials.tids) > 0:
        logger.info('Continue at trial no. {}'.format(len(trials.tids) + 1))
    else:
        hyperopt_store.save_hyperopt_decription(params)
    trials_save_file_path = hyperopt_store.get_filep_hyperopt_trails_obj(params)
    best_trial = hypopt.fmin(f_nn, space, algo=algo_func, max_evals=max_evals,
                             trials=trials, verbose=True, trials_save_file=str(trials_save_file_path))
    hyperopt_store.save_hyperopt_end(params, best_trial)

    logger.info('best_trial: ', best_trial)
    logger.info("Finished")


def _get_func_signature_params(train_mod, algo_func, object_train_func, max_evals):
    params = dict(train_module=misc.get_modul_name_pure(train_mod),
                  func_name=object_train_func, max_evals=max_evals,
                  algo_func=".".join([algo_func.__module__, algo_func.__name__]))
    return params


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
