# -*- coding: utf-8 -*-

from stripe.resource import Customer as StripeCustomer

from ..test import get_test_data, mock_stripe_response


def test_customer(stripe, monkeypatch):
    data = get_test_data('customer/object.json')

    monkeypatch.setattr(StripeCustomer, 'create', mock_stripe_response(data))

    customer = StripeCustomer.create()
    assert customer['id'] == data['id']
