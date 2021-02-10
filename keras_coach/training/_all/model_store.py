
import copy
import pathlib
import yaml
import datetime as dt
import shutil

from keras import models

from _misc_frogs import shortuuid
from _misc_frogs.environment import get_data_dump_root_folder
from _write_read import datetime_to_str
from . import debug

MAX_MDLS_OF_SAME_TYPE_TO_SAFE = 40


def _max_mdls_of_same_type_to_safe():
    global MAX_MDLS_OF_SAME_TYPE_TO_SAFE
    return 3 if debug.HYPEROPT_SIMULATE else MAX_MDLS_OF_SAME_TYPE_TO_SAFE


class ModelBin():

    def __init__(self, dir_=None):
        self.meta_data = None
        self.dir = dir_
        self.model = None

    @property
    def ref_val(self):
        return self.meta_data['reference_value']

    @property
    def length_in_days(self):
        return self.meta_data['length_in_days']

    @property
    def model_build_func(self):
        return self.meta_data['model_build_func']

    @property
    def train_module(self):
        return self.meta_data['train_module']

    @property
    def is_mdl_dir_valid(self):
        base_reqs = (self.get_filep_model_description().is_file()
                     and self.get_filep_model_structure().is_file())
        if debug.HYPEROPT_SIMULATE:
            return base_reqs
        else:
            return (base_reqs and self.get_filep_model_weights().is_file())

    def load_meta_data(self):
        mdl_descr_file = self.get_filep_model_description()
        is_err = False
        with open(mdl_descr_file, 'r') as yaml_file:
            try:
                self.meta_data = yaml.safe_load(yaml_file)
            except yaml.constructor.ConstructorError:
                is_err = True
        if is_err:
            parent = mdl_descr_file.parent
            shutil.rmtree(parent)

    def load_model(self):
        file_ = self.get_filep_model_structure()
        with open(file_, 'r') as yaml_file:
            loaded_model_yaml = yaml_file.read()
        self.model = models.model_from_yaml(loaded_model_yaml)
        # load weights into new model
        file_ = self.get_filep_model_weights()
        self.model.load_weights(file_)
        return self.model

    def safe_model(self, model, params):
        file_ = self.get_filep_model_structure()
        model_yaml = model.to_yaml()
        with open(file_, "w") as yaml_file:
            yaml_file.write(model_yaml)
        # serialize weights to HDF5
        if not debug.HYPEROPT_SIMULATE:
            file_ = self.get_filep_model_weights()
            model.save_weights(file_)
        self._create_info_file(params)

    def _create_info_file(self, params):
        file_ = self.get_filep_model_description()
        params = copy.copy(params)
        params['timestamp'] = datetime_to_str(dt.datetime.now())
        with file_.open("w") as f:
            ydump = yaml.dump(params)
            f.write(ydump)

    def get_filep_model_structure(self):
        file_ = self.dir.joinpath("model_structure.yaml")
        return file_

    def get_filep_model_weights(self):
        file_ = self.dir.joinpath("model_weights.h5")
        return file_

    def get_filep_model_description(self):
        file_ = self.dir.joinpath("model_description.txt")
        return file_


def get_models_sorted_by_reference_value(model_build_func=None, environment=None):
    models = get_models(environment=environment)
    models = sorted(models, key=lambda x: x.ref_val, reverse=True)
    if model_build_func is not None:
        models = [m for m in models if m.model_build_func == model_build_func]
    return models


def get_models(model_ids=None, environment=None):
    models = list()
    mdl_root_dir = _get_model_root_dir(environment)
    if not mdl_root_dir.is_dir():
        return models
    for x in mdl_root_dir.iterdir():
        if not x.is_dir():
            continue
        if model_ids is not None and x.name not in model_ids:
            continue
        mdl = ModelBin(x)
        if mdl.is_mdl_dir_valid:
            mdl.load_meta_data()
            models.append(mdl)
    return models


def save_model(model, params, msg_callb=None):
    assert('train_module' in params)
    assert('model_build_func' in params)
    assert('length_in_days' in params)
    assert('reference_value' in params)

    mdls = get_models_sorted_by_reference_value(params['model_build_func'])
    max_mdls = _max_mdls_of_same_type_to_safe()
    if len(mdls) >= max_mdls \
       and mdls[max_mdls - 1].ref_val > params['reference_value']:
        msg = ("Model not stored, as there are already {} models for '{}' with "
               "bigger reference values."
               .format(max_mdls, params['model_build_func']))
        if msg_callb is None:
            print(msg)
        else:
            msg_callb(msg)
        return

    dir_ = _create_new_mdl_storage_dir_path()
    dir_.mkdir(parents=True, exist_ok=True)
    new_mdl = ModelBin(dir_)
    new_mdl.safe_model(model, params)


def _create_new_mdl_storage_dir_path(environment=None):
    dir_name = shortuuid.uuid()
    mdl_root_dir = _get_model_root_dir(environment)
    dir_ = mdl_root_dir.joinpath(dir_name)
    return dir_


def _get_model_root_dir(environment=None):
    root_dir = get_data_dump_root_folder(environment)
    if debug.HYPEROPT_SIMULATE:
        dir_ = pathlib.Path(root_dir).joinpath("simulate", "models")
    else:
        dir_ = pathlib.Path(root_dir).joinpath("models")
    return dir_
