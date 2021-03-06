# -*- coding: utf-8 -*-
import pytest

from stripe.resource import Customer as StripeCustomer

from ..models import Customer
from ..test import (
    get_test_data,
    mock_stripe_response,
    skip_if_stripe_mock_server_offline,
)


def test_customer_mock(stripe, monkeypatch):
    data = get_test_data('customer/object.json')

    monkeypatch.setattr(StripeCustomer, 'create', mock_stripe_response(data))

    customer = StripeCustomer.create()
    assert customer['id'] == data['id']


@pytest.mark.django_db(transaction=True)
def test_customer_model(stripe, monkeypatch):
    data = get_test_data('customer/object.json')

    monkeypatch.setattr(StripeCustomer, 'create', mock_stripe_response(data))

    customer_object = StripeCustomer.create()

    c = Customer.from_stripe_object(customer_object)
    assert isinstance(c, Customer)
    assert c.id == data['id']


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_customer_model_mock(mock_stripe):
    assert len(mock_stripe.Customer.list().data)
    for customer_object in mock_stripe.Customer.list().auto_paging_iter():
        assert hasattr(customer_object, 'livemode')
        c = Customer.from_stripe_object(customer_object)
        assert isinstance(c, Customer)
