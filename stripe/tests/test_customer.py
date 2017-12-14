# -*- coding: utf-8 -*-

from stripe.resource import convert_to_stripe_object, Customer as StripeCustomer

from ..test import get_test_data


def test_customer(stripe, monkeypatch):
    data = get_test_data('customer/object.json')

    def create_customer(*args, **kwargs):
        return convert_to_stripe_object(data)

    monkeypatch.setattr(StripeCustomer, 'create', create_customer)

    customer = StripeCustomer.create()
    assert customer['id'] == data['id']
