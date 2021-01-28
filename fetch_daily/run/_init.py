import sys
import pathlib
import inspect


def init():
    myp = inspect.getabsfile(lambda: None)
    path = pathlib.Path(myp)
    path = path.joinpath(r"..\..\..\..")
    if path.absolute() not in sys.path:
        sys.path.append(path.absolute())


init()
