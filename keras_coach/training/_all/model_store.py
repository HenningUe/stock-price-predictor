
import copy
import pathlib
import yaml
from keras import models

from _misc_frogs.environment import get_data_dump_root_folder
from _misc_frogs.make_hash import make_hash


def save_model(model, params, results):
    assert('train_module' in params)
    assert('model_build_func' in params)
    assert('epoch' in params)
    assert('length_in_days' in params)
    assert('reference_value' in params)
    dir_ = _get_storage_dir_path(params)
    dir_.mkdir(parents=True, exist_ok=True)
    file_ = _get_filep_model_structure(params)
    if file_.is_file():
        ref_val = _get_stored_reference_value(params)
        if ref_val > params['reference_value']:
            print("Model not stored, as reference is bigger for other model")
            return
    model_yaml = model.to_yaml()
    with open(file_, "w") as yaml_file:
        yaml_file.write(model_yaml)
    # serialize weights to HDF5
    file_ = _get_filep_model_weights(params)
    model.save_weights(file_)
    _create_info_file(params, results)


def load_model(params):
    file_ = _get_filep_model_structure(params)
    with open(file_, 'r') as yaml_file:
        loaded_model_yaml = yaml_file.read()
    model = models.model_from_yaml(loaded_model_yaml)
    # load weights into new model
    file_ = _get_filep_model_weights(params)
    model.load_weights(file_)
    return model


def _get_stored_reference_value(params):
    file_ = _get_filep_model_description(params)
    with file_.open("r") as f:
        ydump = f.read()
        params = yaml.load(ydump)
    return params['reference_value']


def _create_info_file(params, results):
    file_ = _get_filep_model_description(params)
    params = copy.copy(params)
    params['results'] = results
    with file_.open("w") as f:
        ydump = yaml.dump(params)
        f.write(ydump)


def _get_filep_model_structure(params):
    dir_ = _get_storage_dir_path(params)
    file_ = pathlib.Path(dir_).joinpath("model_structure.yaml")
    return file_


def _get_filep_model_weights(params):
    dir_ = _get_storage_dir_path(params)
    file_ = pathlib.Path(dir_).joinpath("model_weights.h5")
    return file_


def _get_filep_model_description(params):
    dir_ = _get_storage_dir_path(params)
    file_ = pathlib.Path(dir_).joinpath("model_description.txt")
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
