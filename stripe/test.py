# -*- coding: utf-8 -*-
import json
import os
from contextlib import contextmanager
import pytest
from django.conf import settings

import stripe
from stripe.resource import convert_to_stripe_object

DATA_DIR = os.path.join(os.path.dirname(__file__), 'tests', 'data')


@contextmanager
def mock_stripe_client():
    old_base = stripe.api_base
    stripe.api_base = 'http://localhost:12111'
    stripe.api_key = 'sk_test_...'

    yield stripe

    stripe.api_base = old_base


def mock_stripe_server_running():
    server_running = True

    with mock_stripe_client() as s:
        try:
            s.Customer.list()
        except stripe.error.APIConnectionError:
            server_running = False

    return server_running


skip_if_stripe_mock_server_offline = pytest.mark.skipif(
    not mock_stripe_server_running(),
    reason='stripe mock server not running'
)


def get_test_stripe_client():
    stripe.api_key = settings.STRIPE_TEST_KEY
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
    return json.load(_file)


def mock_stripe_response(_dict):
    """Mock the response of a stripe API call.

    :param _dict: data of response
    :type _dict: dict
    :rtype: StripeObject
    :returns: Stripe object for the data entered

    Example usage:

        data = get_test_data('customer/object.json')
        monkeypatch.setattr(StripeCustomer, 'create', mock_stripe_response(data))

        customer = StripeCustomer.create()
        assert customer['id'] == data['id']
    """
    def callback(*args, **kwargs):
        return convert_to_stripe_object(_dict)
    return callback
