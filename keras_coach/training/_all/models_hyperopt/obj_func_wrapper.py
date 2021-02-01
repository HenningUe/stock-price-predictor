
from keras import models, layers, optimizers, metrics, regularizers  # @UnusedImport
import hyperopt as hypopt

from _misc_frogs import loggermod
from keras_coach.training._all import model_store, traindata, debug


def get_objective_func_wrapped(train_module):
    obj_func_bin = ObjectiveFuncBin(train_module)
    return obj_func_bin.objective_func


class ObjectiveFuncBin:

    def __init__(self, train_module):
        self.train_module = train_module

    def objective_func(self, params):
        logger = loggermod.get_logger()
        data_day_len = params['data_day_len']
        if debug.HYPEROPT_SIMULATE:
            logger.info("data_day_len: {}".format(data_day_len))
            data_day_len = 3
        x_train_data, y_label_df_raw = traindata.get_training_data(data_day_len)

        func_params = params['mdlfuncs'] if 'mdlfuncs' in params else params
        try:
            rtn = self.train_module.objective_func(x_train_data, y_label_df_raw, func_params)
            model = rtn['model']
            save_mdl_params = rtn['save_mdl_params']
            if save_mdl_params is not None:
                train_mod_name = self.train_module.__name__.split('.')[-1]
                save_mdl_params.update(dict(train_module=train_mod_name,
                                            model_build_func=func_params['funcname'],
                                            length_in_days=params['data_day_len']))

                if not debug.HYPEROPT_SIMULATE:
                    model_store.save_model(model, save_mdl_params, rtn['acc'])
            obj_func_rtn = dict(loss=rtn['acc'], status=hypopt.STATUS_OK)
        except Exception as ex:
            logger.exception(ex)
            logger.error("function: {}".format(func_params['funcname']))
            logger.error("related params:")
            logger.error(func_params)
            obj_func_rtn = dict(status=hypopt.STATUS_FAIL)

        logger.info("Finished '{}'. Return: {}".format(func_params['funcname'], obj_func_rtn))
        return obj_func_rtn
