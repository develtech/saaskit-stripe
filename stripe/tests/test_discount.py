# -*- coding: utf-8 -*-
import json

import pytest

import responses
import stripe

from ..models import Discount
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@responses.activate
@pytest.mark.django_db(transaction=True)
def test_customer_discount_percent_model_mock(mock_stripe):
    customer = {
        'account_balance': 0,
        'created': 1513262366,
        'currency': 'usd',
        'default_source': 'card_1BYxtEEzushJqDoiJUQkSyER',
        'delinquent': False,
        'description': 'Test user',
        'discount': {
            'coupon': {
                'amount_off': None,
                'created': 1513530930,
                'currency': None,
                'duration': 'once',
                'duration_in_months': None,
                'id': 'half-off',
                'livemode': False,
                'max_redemptions': None,
                'metadata': {},
                'object': 'coupon',
                'percent_off': 50,
                'redeem_by': None,
                'times_redeemed': 1,
                'valid': True
            },
            'customer': 'cus_Bwrbeyo88aaUYP',
            'end': None,
            'object': 'discount',
            'start': 1513530963,
            'subscription': None
        },
        'email': 'tony@git-pull.com',
        'id': 'cus_Bwrbeyo88aaUYP',
        'livemode': False,
        'metadata': {},
        'object': 'customer',
        'shipping': None,
        'sources': [],
        'subscriptions': {
            'data': [],
            'has_more': False,
            'object': 'list',
            'total_count': 0,
            'url': '/v1/customers/cus_Bwrbeyo88aaUYP/subscriptions'
        }
    }

    customer_id = customer['id']
    customer_url = stripe.api_base + '/v1/customers/%s' % customer_id
    customer_json = json.dumps(customer)
    responses.add(
        responses.GET,
        customer_url,
        body=customer_json,
        status=200,
        content_type='application/json',
    )

    customer_object = stripe.Customer.retrieve(customer_id)

    assert hasattr(customer_object, 'discount')

    s = Discount.from_stripe_object(customer_object.discount)
    assert isinstance(s, Discount)


@skip_if_stripe_mock_server_offline
@responses.activate
@pytest.mark.django_db(transaction=True)
def test_customer_discount_amount_off_model_mock(mock_stripe):
    customer = {
        'account_balance': 0,
        'created': 1513262366,
        'currency': 'usd',
        'default_source': 'card_1BYxtEEzushJqDoiJUQkSyER',
        'delinquent': False,
        'description': 'Test user',
        'discount': {
            'coupon': {
                'amount_off': 1500,
                'created': 1513532343,
                'currency': 'usd',
                'duration': 'once',
                'duration_in_months': None,
                'id': '15-off',
                'livemode': False,
                'max_redemptions': 5,
                'metadata': {},
                'object': 'coupon',
                'percent_off': None,
                'redeem_by': 1515650399,
                'times_redeemed': 1,
                'valid': True
            },
            'customer': 'cus_Bwrbeyo88aaUYP',
            'end': None,
            'object': 'discount',
            'start': 1513532388,
            'subscription': None
        },
        'email': 'tony@git-pull.com',
        'id': 'cus_Bwrbeyo88aaUYP',
        'livemode': False,
        'metadata': {},
        'object': 'customer',
        'shipping': None,
        'sources': [],
        'subscriptions': {
            'data': [],
            'has_more': False,
            'object': 'list',
            'total_count': 0,
            'url': '/v1/customers/cus_Bwrbeyo88aaUYP/subscriptions'
        }
    }

    customer_id = customer['id']
    customer_url = stripe.api_base + '/v1/customers/%s' % customer_id
    customer_json = json.dumps(customer)
    responses.add(
        responses.GET,
        customer_url,
        body=customer_json,
        status=200,
        content_type='application/json',
    )

    customer_object = stripe.Customer.retrieve(customer_id)

    assert hasattr(customer_object, 'discount')

    s = Discount.from_stripe_object(customer_object.discount)
    assert isinstance(s, Discount)


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
@pytest.mark.skip(reason='wait')
def test_subscription_discount_model_mock(mock_stripe):
    subscription_list = mock_stripe.Subscription.list()
    for stripe_object in subscription_list.auto_paging_iter():
        s = Discount.from_stripe_object(stripe_object, stripe_object.discount)
        assert isinstance(s, Discount)
