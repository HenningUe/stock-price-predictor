#!/usr/bin/env python
# encoding: utf-8
#
# pmatic - Python API for Homematic. Easy to use.
# Copyright (C) 2016 Lars Michelsen <lm@larsmichelsen.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

# Add Python 3.x behaviour to 2.7
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    from urllib.request import urlopen
    from urllib.error import URLError
except ImportError:
    from urllib2 import urlopen
    from urllib2 import URLError  # @UnusedImport

try:
    # Python 2
    from urllib import urlencode
except ImportError:
    # Python 3+
    from urllib.parse import urlencode

import json


class Pushover(object):
    """This notification class is used to send out notifications using Pushover (pushover.net).

    The API to this notification class is pretty simple. You normally only need to care
    about using the :meth:`send` class method. One example::

        Pushover.send("This is the message to send :-)",
                      api_token="xdrvcc6svnbFQ0hmAx4tDhbWU8nDK6",
                      user_token="go8cCpgmWdAmbj2jpm4TmdzoHpVUjH")

    For details take a look below.
    """

    _api_token = None
    _user_token = None

    @classmethod
    def send(cls, message, title=None, api_token=None, user_token=None):
        """Send a notification via pushover.net.

        This class method can be used to send out custom notifiations to your tablet or
        mobile phone using pushover.net. To be able to send such notifications you need
        to register with pushover.net, register your appliation to obtaion an API token
        and a user or group token.

        If you have both, you can use this class method to send a notification containing
        only a *message*. But you can also provide an optional *title*.

        It returns ``True`` when the notification has been sent or raises a
        :class:`.pmatic.Exception` when either an invalid *message* or *title* is provided.
        In case of errors during sending the notification, a :class:`.pmatic.Exception`
        is raised.
        """
        api_token, user_token = cls._load_tokens(api_token, user_token)

        if not message:
            raise ValueError("A message has to be specified.")

        if not isinstance(title, str):
            raise ValueError("The message needs to be a unicode string.")

        encoded_msg = message.encode("utf-8")
        if len(encoded_msg) > 1024:
            raise ValueError("The message exceeds the maximum length of 1024 characters.")

        msg = [
            ("token", api_token.encode("utf-8")),
            ("user", user_token.encode("utf-8")),
            ("message", encoded_msg),
        ]

        if title is not None:
            if not isinstance(title, str):
                raise ValueError("The title needs to be a unicode string.")

            encoded_title = title.encode("utf-8")
            if len(encoded_title) > 250:
                raise ValueError("The title exceeds the maximum length of 250 characters.")
            msg.append(("title", encoded_title))

        handle = urlopen("https://api.pushover.net/1/messages.json",
                         data=urlencode(msg).encode("utf-8"))
        return cls._check_response(handle)

    @classmethod
    def _check_response(cls, handle):
        if handle.getcode() != 200:
            raise ValueError("Got invalid HTTP status code: %d" % (handle.getcode()))

        response_body = handle.read().decode("utf-8")

        data = json.loads(response_body)
        if data["status"] != 1:
            raise ValueError("Got invalid response (%d): %s" % (data["status"], response_body))

        return True

    @classmethod
    def _load_tokens(cls, api_token, user_token):
        if api_token is None:
            api_token = cls._api_token

        if api_token is None:
            raise ValueError("You need to either set the default tokens or provide your "
                             "API token with the api_token argument.")

        if user_token is None:
            user_token = cls._user_token

        if user_token is None:
            raise ValueError("You need to either set the default tokens or provide your "
                             "User/Group token with the user_token argument.")

        return api_token, user_token

    @classmethod
    def set_default_tokens(cls, api_token, user_token):
        """Set default pushover credentials.

        They can be set e.g. on startup of your program. If you set the default tokens here,
        you don't need to provide the tokens on every :meth:`send` call. The tokens provided as
        arguments to :meth:`send` are overriding the tokens set with this method."""
        cls._api_token = api_token
        cls._user_token = user_token
