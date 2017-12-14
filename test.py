# -*- coding: utf-8 -*-
import json
import os

import stripe


DATA_DIR = os.path.join(os.path.dirname(__file__), 'tests', 'data')


def get_mock_stripe_client():
    stripe.api_base = 'http://localhost:12111'
    stripe.api_key = 'sk_test_...'
    return stripe


def get_test_stripe_client():
    stripe.api_key = 'sk_test_BQokikJOvBiI2HlWgH4olfQ2'
    return stripe


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
