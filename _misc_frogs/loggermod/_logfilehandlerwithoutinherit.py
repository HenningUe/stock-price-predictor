
from ctypes import *
import msvcrt


def _open(self):
    """
    Open the current base file with the (original) mode and encoding.
    Return the resulting stream.
    """
    if self.encoding is None:
        stream = open(self.baseFilename, self.mode)
        handle = msvcrt.get_osfhandle(stream.fileno())
        windll.kernel32.SetHandleInformation(handle, 1, 0)  # @UndefinedVariable
    else:
        stream = open(self.baseFilename, self.mode, self.encoding)
    return stream


import logging  # @IgnorePep8
logging.FileHandler._open = _open
