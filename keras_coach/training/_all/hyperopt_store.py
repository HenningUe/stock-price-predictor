
import pathlib
import yaml
import pickle

from _misc_frogs.environment import get_data_dump_root_folder
from _misc_frogs.make_hash import make_hash
from . import debug


def save_hyperopt_decription(params, suffix=""):
    dir_ = _get_storage_dir_path(params)
    dir_.mkdir(parents=True, exist_ok=True)
    # hyperopt_description
    file_ = _get_filep_hyperopt_description(params, suffix)
    with file_.open("w") as f:
        ydump = yaml.dump(params)
        f.write(ydump)


def save_hyperopt_end(params, best_trial):
    dir_ = _get_storage_dir_path(params)
    dir_.mkdir(parents=True, exist_ok=True)
    # hyperopt_description
    save_hyperopt_decription(params, "finish")
    # hyperopt_best_trial
    file_ = _get_filep_hyperopt_best_trial(params)
    with file_.open("w") as f:
        ydump = yaml.dump(best_trial)
        f.write(ydump)


def save_hyperopt_trials(params, trials_obj):
    file_ = get_filep_hyperopt_trails_obj(params)
    with file_.open("wb") as f:
        pickle.dump(trials_obj, f)


def load_hyperopt_trial(params):
    file_ = get_filep_hyperopt_trails_obj(params)
    if not file_.is_file():
        return None
    with file_.open("rb") as f:
        trials_obj = pickle.load(f)
    return trials_obj


def delete_hyperopt_trial(params):
    file_ = get_filep_hyperopt_trails_obj(params)
    file_.unlink(missing_ok=True)


def get_filep_hyperopt_trails_obj(params):
    dir_ = _get_storage_dir_path(params)
    file_ = pathlib.Path(dir_).joinpath("hyperopt_trials_obj.pkl")
    return file_


def _get_filep_hyperopt_description(params, suffix):
    dir_ = _get_storage_dir_path(params)
    if suffix:
        suffix = "_" + suffix
    file_ = pathlib.Path(dir_).joinpath(f"hyperopt_description{suffix}.yaml")
    return file_


def _get_filep_hyperopt_best_trial(params):
    dir_ = _get_storage_dir_path(params)
    file_ = pathlib.Path(dir_).joinpath("hyperopt_besttrial.yaml")
    return file_


def _get_storage_dir_path(params):
    assert('train_module' in params)
    assert('max_evals' in params)
    assert('algo_func' in params)
    paramsx = dict(train_module=params['train_module'],
                   algo_func=params['algo_func'],)
    if 'func_name' in params:
        paramsx['func_name'] = params['func_name']

    hash_val = _get_hash(paramsx)
    root_dir = get_data_dump_root_folder()
    if debug.HYPEROPT_SIMULATE:
        dir_ = pathlib.Path(root_dir).joinpath("simulate", "hyperopt", hash_val)
    else:
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
