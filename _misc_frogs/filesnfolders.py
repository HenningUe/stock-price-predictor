
import pathlib
import inspect


def get_storage_root_folder():
    myfile = inspect.getabsfile(lambda: None)
    lastdir = pathlib.Path(myfile).parent
    cdir = lastdir
    while True:
        r_path = cdir.joinpath("datafrog")
        if r_path.is_dir():
            break
        r_path = None
        cdir = cdir.parent
        if cdir == lastdir:
            break
        lastdir = cdir
    if r_path is not None:
        return r_path
