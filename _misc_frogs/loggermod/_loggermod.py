# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from _misc_frogs import str_rescue
from _misc_frogs.environment import get_data_dump_root_folder
from . import _logfilehandlerwithoutinherit  # @UnusedImport

_singleton = None
LOGGER_NAME_DEFAULT = "StockFrog"


def init_logger(logger_name=None):
    global _singleton, LOGGER_NAME_DEFAULT
    if _singleton is None:
        if logger_name is None:
            logger_name = "StockFrog"
        _singleton = LoggerClass(logger_name)


def get_logger(logger_name=None):
    global _singleton
    if _singleton is None:
        init_logger(logger_name)
    return _singleton


class LoggerClass(object):

    def __init__(self, logger_name):
        self.logger = None
        self.logger_name = logger_name
        self._set_up_logger1()

    def info(self, msg, *args, **kwargs):
        msg = str_rescue.make_safe_unicode_from_anything(msg)
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.warning(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        msg = str_rescue.make_safe_unicode_from_anything(msg)
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        msg = str_rescue.make_safe_unicode_from_anything(msg)
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        msg = str_rescue.make_safe_unicode_from_anything(msg)
        self.logger.exception(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        msg = str_rescue.make_safe_unicode_from_anything(msg)
        self.logger.debug(msg, *args, **kwargs)

    def set_debug_level(self):
        for hdl in self.logger.handlers:
            hdl.setLevel(logging.DEBUG)

    def _set_up_logger1(self):
        self.logger = logging.getLogger(self.logger_name)
        # self.logger.addFilter(_RemoveDuplicateFilter())r
        if len(self.logger.handlers) > 1:
            return
        self.logger.setLevel(logging.INFO)

        # File-Handler for Info
        log_dir = self._get_logger_path()
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file_fullfilepath = log_dir.joinpath(self.logger_name + u".log.txt")
        fh1 = RotatingFileHandler2(str(log_file_fullfilepath), maxBytes=6 * 1024, backupCount=2)
        self._set_default_formatter(fh1)
        self.logger.addHandler(fh1)

        # File-Handler for Error
        log_dir = self._get_logger_path()
        log_dir = log_dir.joinpath(u"error")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file_fullfilepath = log_dir.joinpath(self.logger_name + u"_error.log.txt")
        fh2 = RotatingFileHandler2(str(log_file_fullfilepath), maxBytes=6 * 1024, backupCount=2)
        self._set_default_formatter(fh2)
        fh2.setLevel(logging.ERROR)  # @UndefinedVariable
        self.logger.addHandler(fh2)

        # Console-Handler
        consoleh = StreamHandler2(stream=sys.stdout)
        self._set_default_formatter(consoleh)
        self.logger.addHandler(consoleh)

    @staticmethod
    def _set_default_formatter(handler):
        formatter_msg = (u'%(asctime)s, %(levelname)s: %(message)s')
        formatter = logging.Formatter(formatter_msg, u"%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)

    def _get_logger_path(self):
        REL_LOG_PATH = r'logs'
        storage_root = get_data_dump_root_folder()
        log_dir = storage_root.joinpath(REL_LOG_PATH)
        return log_dir


class RotatingFileHandler2(RotatingFileHandler):

    def doRollover(self):  # @NOSONAR
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            filename, ext = os.path.splitext(self.baseFilename)
            filename_for_id = u"{}.{{}}{}".format(filename, ext)
            for i in range(self.backupCount - 1, 0, -1):
                sfn = filename_for_id.format(i)
                dfn = filename_for_id.format(i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = filename_for_id.format("1")
            if os.path.exists(dfn):
                os.remove(dfn)
            # Issue 18940: A file may not have been created if delay is True.
            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
        if not getattr(self, 'delay', 0):
            self.stream = self._open()


class StreamHandler2(logging.StreamHandler):

    def emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.format(record)
            stream = self.stream
            fs = "%s\n"
            try:
                if (isinstance(msg, bytes) and getattr(stream, 'encoding', None)):
                    ufs = u'%s\n'
                    try:
                        self._write(ufs % msg)
                        # stream.write(ufs % msg)
                    except UnicodeEncodeError:
                        # Printing to terminals sometimes fails. For example,
                        # with an encoding of 'cp1251', the above write will
                        # work if written to a stream opened or wrapped by
                        # the codecs module, but fail when writing to a
                        # terminal even when the codepage is set to cp1251.
                        # An extra encoding step seems to be needed.
                        stream.write((ufs % msg).encode(stream.encoding))
                else:
                    self._write(fs % msg)
                    # stream.write(fs % msg)
            except UnicodeError:
                self._write(fs % msg.encode("UTF-8"))
                # stream.write(fs % msg.encode("UTF-8"))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

    def _write(self, text, retry=5):
            # Workaround for Windows 10 console bug:
            # https://github.com/robotframework/robotframework/issues/2709
            try:
                self.stream.write(text)
            except IOError as err:
                if not (err.errno == 0 and retry > 0):
                    raise
                self._write(text, retry - 1)
