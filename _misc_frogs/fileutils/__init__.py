#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import win32con
import win32api
import subprocess
import time


def get_temp_folder(create_folder=True):
    NAME = u"_temp"
    mypath = os.path.split(sys.argv[0])[0]
    temp_path = os.path.join(mypath, NAME)
    if not os.path.isdir(temp_path) and create_folder:
        os.mkdir(temp_path)
    elif not os.path.isdir(temp_path) and not create_folder:
        temp_path = None
    return temp_path


def get_local_app_data_path():
    return os.environ[u'LOCALAPPDATA']


def file_is_hidden(filepath):
    attrs = win32api.GetFileAttributes(filepath)
    return (attrs & win32con.FILE_ATTRIBUTE_HIDDEN)


def file_is_system(filepath):
    attrs = win32api.GetFileAttributes(filepath)
    return (attrs & win32con.FILE_ATTRIBUTE_SYSTEM)


def file_is_archive(filepath):
    attrs = win32api.GetFileAttributes(filepath)
    return attrs & win32con.FILE_ATTRIBUTE_ARCHIVE


def file_is_readonly(filepath):
    attrs = win32api.GetFileAttributes(filepath)
    return attrs & win32con.FILE_ATTRIBUTE_READONLY


def file_copy_with_xcopy(src_file, dst_file):
    cmd = [u"xcopy", u"/C", u"/Y", u"/H", u"/R", src_file, dst_file]
    subprocess.call(cmd)
