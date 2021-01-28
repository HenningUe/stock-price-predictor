
import pathlib
import pickle
import yaml
import functools

from _misc_frogs.environment import get_data_source_root_folder
from _misc_frogs.make_hash import make_hash

_Y_M_D_STRF = "%Y-%m-%d"


def get_cached_data_deco(func_outer):

    @functools.wraps(func_outer)
    def func_inner(data_set_spec, date_start=None, date_end=None, time_range=None,
                   sample_period_in_min=5, overlapping=True):
        data = _get_cached_data(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping)
        if data is None:
            data = func_outer(data_set_spec, date_start, date_end, time_range,
                              sample_period_in_min, overlapping)
            _store_data_in_cache(data, data_set_spec, date_start, date_end, time_range,
                                 sample_period_in_min, overlapping)
        return data

    return func_inner


def _get_cached_data(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping):
    file_ = _get_storage_file_path(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping)
    data = None
    if file_.is_file():
        with file_.open("rb") as f:
            data = pickle.load(f)
    return data


def _store_data_in_cache(data, data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping):
    file_ = _get_storage_file_path(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping)

    if not file_.parent.is_dir():
        file_.parent.mkdir(parents=True)
    with file_.open("wb") as f:
        pickle.dump(data, f)
    _create_info_file(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping)


def _create_info_file(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping):
    global _Y_M_D_STRF
    date_start_str = "<NONE>" if date_start is None else date_start.strftime(_Y_M_D_STRF)
    date_end_str = "<NONE>" if date_end is None else date_end.strftime(_Y_M_D_STRF)
    data = dict(date_start=date_start_str,
                date_end=date_end_str,
                symbols=[s['name'] for s in data_set_spec['symbols']],
                label_symbol=data_set_spec['label_symbol'],
                time_range=str(time_range),
                sample_period_in_min=str(sample_period_in_min),
                overlapping=overlapping)
    dir_ = _get_storage_dir_path(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping)
    file_ = pathlib.Path(dir_).joinpath("cached_data.txt")
    with file_.open("w") as f:
        ydump = yaml.dump(data)
        f.write(ydump)


def _get_storage_file_path(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping):
    dir_ = _get_storage_dir_path(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping)
    file_ = pathlib.Path(dir_).joinpath("cached_data.pkl")
    return file_


def _get_storage_dir_path(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping):
    hash_val = _get_hash(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping)
    root_dir = get_data_source_root_folder()
    dir_ = pathlib.Path(root_dir).joinpath("cached", hash_val)
    return dir_


def _get_hash(data_set_spec, date_start, date_end, time_range, sample_period_in_min, overlapping):
    global _Y_M_D_STRF
    # length_in_days
    len_in_days = data_set_spec['length_in_days']
    hash_ = make_hash(str(len_in_days))
    # label_symbol
    label_symbol = data_set_spec['label_symbol']
    hash_ = hash_ ^ make_hash("LS" + label_symbol)
    # sample_period_in_min
    hash_ = hash_ ^ make_hash(str(sample_period_in_min))
    # symbols
    symbs = "_".join(s['name'] for s in data_set_spec['symbols'])
    hash_ = hash_ ^ make_hash(symbs)
    # date_start
    date_start_str = "<NONE>" if date_start is None else date_start.strftime(_Y_M_D_STRF)
    hash_ = hash_ ^ make_hash(date_start_str)
    # date_end
    date_end_str = "<NONE>" if date_end is None else date_end.strftime(_Y_M_D_STRF)
    hash_ = hash_ ^ make_hash(date_end_str)
    # time_range
    hash_ = hash_ ^ make_hash(str(time_range))
    # overlapping
    hash_ = hash_ ^ make_hash("ov" if overlapping else "nov")
    return hex(hash_)[2:]
