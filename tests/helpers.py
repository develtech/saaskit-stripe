# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import json


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def open_test_file(_filename, path=DATA_DIR):
    """Open data file for tests.

    :param _filename: name of file to load
    :type _filename: str
    :param path: path of file, defaults to DATA_DIR
    :type path: str
    :returns: test data file
    :rtype: :py:term:`file object`
    """
    return open(os.path.join(path, _filename))


def json_file_to_dict(_file):
    """Return dict from json file.

    :param _file: json file
    :type _file: file object
    :returns: dictionary
    :rtype: :class:`dict`

    """
    return json.load(_file)


def get_test_data(_filename, path=DATA_DIR):
    """Return dict of test data.

    :param _filename: name of file to load
    :type _filename: str
    :param path: path of file, defaults to DATA_DIR
    :type path: str
    :returns: dictionary
    :rtype: :class:`dict`
    """
    _file = open_test_file(_filename, path)
    return json_file_to_dict(_file)
