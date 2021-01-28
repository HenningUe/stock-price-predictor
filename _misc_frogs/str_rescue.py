# -*- coding: utf-8 -*-

import sys
import unicodedata


def try_unicode_conversion(str_in, default_encoding=None):
    if isinstance(str_in, bytes):
        if is_utf8_strict(str_in):
            return str_in.decode("utf-8")
        code_tries = [sys.getfilesystemencoding(),
                      "latin-1", "iso8859-1", "utf-16",
                      sys.getdefaultencoding()]
        if default_encoding is not None:
            code_tries.insert(0, default_encoding)
        for i_try, code in enumerate(code_tries):
            try:
                str_in = str_in.decode(code)
                break
            except UnicodeDecodeError:
                if i_try == len(code_tries) - 1:
                    raise
                continue
    return str_in


def make_safe_unicode_from_anything(str_in, default_encoding=None):
    if not isinstance(str_in, (str, bytes)):
        try:
            str_in = str(str_in)
        except UnicodeError:
            str_in = bytes(str_in)
    str_in = try_unicode_conversion(str_in, default_encoding)
    return make_safe_str(str_in)


def is_utf8_strict(data):
    try:
        decoded = data.decode('UTF-8')
    except UnicodeDecodeError:
        return False
    else:
        for ch in decoded:
            if 0xD800 <= ord(ch) <= 0xDFFF:
                return False
        return True


def make_safe_str(str_in):
    if not isinstance(str_in, str):
        raise TypeError(u"Parameter 'str_in' must be of type 'bytes'. "
                        u"However, parameter is of type '{}'".
                        format(type(str_in)))
    str_in = _replace_german_special_chars(str_in)
    str_in = _replace_other_special_chars(str_in)
    str_in = _replace_chars_with_accents(str_in)
    str_in = _remove_any_non_ascii_char(str_in)
    return str_in


def _replace_german_special_chars(str_in):
    str_in = str_in.replace(u'Ä', u'Ae')
    str_in = str_in.replace(u'ä', u'ae')
    str_in = str_in.replace(u'Ö', u'Oe')
    str_in = str_in.replace(u'ö', u'oe')
    str_in = str_in.replace(u'Ü', u'Ue')
    str_in = str_in.replace(u'ü', u'ue')
    str_in = str_in.replace(u'ß', u'ss')
    return str_in


def _replace_other_special_chars(str_in):
    str_in = str_in.replace(u'€', u'Euro')
    str_in = str_in.replace(u'µ', u'u')
    str_in = str_in.replace(u'ñ', u'ny')
    return str_in


def _replace_chars_with_accents(str_in):
    nkfd_form = unicodedata.normalize(u'NFKD', str_in)
    return u''.join(c for c in nkfd_form if not unicodedata.combining(c))


def _remove_any_non_ascii_char(str_in):
    return str_in.encode(u'ascii', u'replace').decode()


if __name__ == u"__main__":
    str_s = u"Ceñía is und für daß @µ ² geméinê à und ê ´ ` ° xx"
    str_s = make_safe_str(str_s)
    print(type(str_s))
    print(str_s)
    str_s = u"Ceñía is und für daß @µ ² geméinê à und ê ´ ` ° xx".encode("iso8859-1")
    print(make_safe_unicode_from_anything(str_s))
