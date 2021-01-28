
import sys
import pathlib
import inspect


def _add_libs_to_sys_path():
    my_file = inspect.getabsfile(lambda: None)
    my_file = pathlib.Path(my_file)
    root_dir = my_file.parent.parent
    lib_dir = root_dir.joinpath("_libs")
    lib_dir = str(lib_dir)
    if lib_dir not in sys.path:
        sys.path.append(lib_dir)


_add_libs_to_sys_path()
