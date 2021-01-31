
import sys


def _open(self):
    """
    Open the current base file with the (original) mode and encoding.
    Return the resulting stream.
    """
    import ctypes
    import msvcrt
    if self.encoding is None:
        stream = open(self.baseFilename, self.mode)
        handle = msvcrt.get_osfhandle(stream.fileno())
        ctypes.windll.kernel32.SetHandleInformation(handle, 1, 0)  # @UndefinedVariable
    else:
        stream = open(self.baseFilename, self.mode, self.encoding)
    return stream


def _replace_log_filehdl_open():
    import logging  # @IgnorePep8
    if "win" in sys.platform.lower():
        logging.FileHandler._open = _open


_replace_log_filehdl_open()
