
import copy
import pathlib
import yaml
import pickle

from _misc_frogs.environment import get_data_dump_root_folder
from _misc_frogs.make_hash import make_hash


def save_hyperopt_ex(ex):
    pass


def save_hyperopt_trial(params, best_trial, trials_obj):
    assert('train_module' in params)
    assert('max_evals' in params)
    assert('algo_func' in params)

    dir_ = _get_storage_dir_path(params)
    dir_.mkdir(parents=True, exist_ok=True)
    # hyperopt_description
    file_ = _get_filep_hyperopt_description(params)
    with file_.open("w") as f:
        ydump = yaml.dump(params)
        f.write(ydump)
    # hyperopt_best_trial
    file_ = _get_filep_hyperopt_best_trial(params)
    with file_.open("w") as f:
        ydump = yaml.dump(best_trial)
        f.write(ydump)
    # hyperopt_trails_obj
    file_ = _get_filep_hyperopt_trails_obj(params)
    with file_.open("wb") as f:
        pickle.dump(trials_obj, f)


def _get_filep_hyperopt_trails_obj(params):
    dir_ = _get_storage_dir_path(params)
    file_ = pathlib.Path(dir_).joinpath("hyperopt_trials_obj.pkl")
    return file_


def _get_filep_hyperopt_description(params):
    dir_ = _get_storage_dir_path(params)
    file_ = pathlib.Path(dir_).joinpath("hyperopt_description.yaml")
    return file_


def _get_filep_hyperopt_best_trial(params):
    dir_ = _get_storage_dir_path(params)
    file_ = pathlib.Path(dir_).joinpath("hyperopt_besttrial.yaml")
    return file_


def _get_storage_dir_path(params):
    params = copy.copy(params)
    params.pop('max_evals')
    hash_val = _get_hash(params)
    root_dir = get_data_dump_root_folder()
    dir_ = pathlib.Path(root_dir).joinpath("hyperopt", hash_val)
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
