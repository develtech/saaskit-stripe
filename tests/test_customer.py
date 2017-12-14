# -*- coding: utf-8 -*-

from stripe.resource import Customer as StripeCustomer

from ..models import Customer
from ..test import get_test_data, mock_stripe_response


def test_customer_mock(stripe, monkeypatch):
    data = get_test_data('customer/object.json')

    monkeypatch.setattr(StripeCustomer, 'create', mock_stripe_response(data))

    customer = StripeCustomer.create()
    assert customer['id'] == data['id']


def test_customer_model(stripe, monkeypatch):
    data = get_test_data('customer/object.json')

    monkeypatch.setattr(StripeCustomer, 'create', mock_stripe_response(data))

    customer = StripeCustomer.create()
    cdict = customer.to_dict()
    cdict.pop('object')
    cdict.pop('subscriptions')
    c = Customer(**cdict)
