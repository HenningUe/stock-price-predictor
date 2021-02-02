
import copy
import pathlib
import yaml
import datetime as dt

from keras import models

from _misc_frogs.environment import get_data_dump_root_folder
from _misc_frogs.make_hash import make_hash
from _write_read import datetime_to_str


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

    def load_meta_data(self):
        mdl_descr_file = _get_filep_model_description(self.dir)
        with open(mdl_descr_file, 'r') as yaml_file:
            self.meta_data = yaml_file.read()

    def load_model(self):
            self.model = load_model(self.dir)


def get_models_sorted_by_reference_value(model_build_func=None):
    models = get_models()
    models = sorted(models, key=lambda x: x.ref_val)
    if model_build_func is not None:
        models = [m for m in models if m.model_build_func == model_build_func]
    return models


def get_models():
    models = list()
    root_dir = get_data_dump_root_folder()
    for x in root_dir.iterdir():
        if not x.is_dir():
            continue
        mdl = ModelBin(x)
        mdl.load_meta_data()
        models.append(mdl)
    return models


def save_model(model, params, results):
    assert('train_module' in params)
    assert('model_build_func' in params)
    assert('epoch' in params)
    assert('length_in_days' in params)
    assert('reference_value' in params)
    dir_ = _get_storage_dir_path(params)
    dir_.mkdir(parents=True, exist_ok=True)
    file_ = _get_filep_model_structure_via_params(params)
    if file_.is_file():
        ref_val = _get_stored_reference_value(params)
        if ref_val > params['reference_value']:
            print("Model not stored, as reference is bigger for other model")
            return
    model_yaml = model.to_yaml()
    with open(file_, "w") as yaml_file:
        yaml_file.write(model_yaml)
    # serialize weights to HDF5
    file_ = _get_filep_model_weights_via_params(params)
    model.save_weights(file_)
    _create_info_file(params, results)


def load_model(dir_):
    file_ = _get_filep_model_structure(dir_)
    with open(file_, 'r') as yaml_file:
        loaded_model_yaml = yaml_file.read()
    model = models.model_from_yaml(loaded_model_yaml)
    # load weights into new model
    file_ = _get_filep_model_weights(dir_)
    model.load_weights(file_)
    return model


def _get_stored_reference_value(params):
    file_ = _get_filep_model_description_via_params(params)
    with file_.open("r") as f:
        params = yaml.safe_load(f)
    return params['reference_value']


def _create_info_file(params, results):
    file_ = _get_filep_model_description_via_params(params)
    params = copy.copy(params)
    params['results'] = results
    params['timestamp'] = datetime_to_str(dt.datetime.now())
    with file_.open("w") as f:
        ydump = yaml.dump(params)
        f.write(ydump)


def _get_filep_model_structure_via_params(params):
    dir_ = _get_storage_dir_path(params)
    return _get_filep_model_structure(dir_)


def _get_filep_model_structure(mdl_dir):
    file_ = mdl_dir.joinpath("model_structure.yaml")
    return file_


def _get_filep_model_weights_via_params(params):
    dir_ = _get_storage_dir_path(params)
    return _get_filep_model_weights(dir_)


def _get_filep_model_weights(mdl_dir):
    file_ = mdl_dir.joinpath("model_weights.h5")
    return file_


def _get_filep_model_description_via_params(params):
    dir_ = _get_storage_dir_path(params)
    return _get_filep_model_description(dir_)


def _get_filep_model_description(mdl_dir):
    file_ = mdl_dir.joinpath("model_description.txt")
    return file_


def _get_storage_dir_path(params):
    params = copy.copy(params)
    params.pop('reference_value')
    hash_val = _get_hash(params)
    root_dir = get_data_dump_root_folder()
    dir_ = pathlib.Path(root_dir).joinpath("models", hash_val)
    return dir_


def _get_hash(params):
    hash_ = None
    for param_name in params:
        val = params[param_name]
        if hash_ is None:
            hash_ = make_hash(str(val))
        else:
            hash_ = hash_ ^ make_hash(str(val))
    return hex(hash_)[2:]
