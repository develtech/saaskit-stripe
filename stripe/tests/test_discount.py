# -*- coding: utf-8 -*-
import json

import pytest

import responses
import stripe

from ..models import Discount
from ..test import skip_if_stripe_mock_server_offline


@responses.activate
@skip_if_stripe_mock_server_offline
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


@responses.activate
@skip_if_stripe_mock_server_offline
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


@responses.activate
@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_subscription_discount_model_mock(mock_stripe):

    subscription = {
        'application_fee_percent': None,
        'billing': 'charge_automatically',
        'cancel_at_period_end': False,
        'canceled_at': None,
        'created': 1513273056,
        'current_period_end': 1515951456,
        'current_period_start': 1513273056,
        'customer': 'cus_Bwrbeyo88aaUYP',
        'days_until_due': None,
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
                'times_redeemed': 2,
                'valid': True
            },
            'customer': 'cus_Bwrbeyo88aaUYP',
            'end': None,
            'object': 'discount',
            'start': 1513532569,
            'subscription': 'sub_BwuTCVDt1Klbil'
        },
        'ended_at': None,
        'id': 'sub_BwuTCVDt1Klbil',
        'items': {
            'data': [{
                'created': 1513273056,
                'id': 'si_BwuToPkPLdw9g0',
                'metadata': {},
                'object': 'subscription_item',
                'plan': {
                    'amount': 999,
                    'created': 1513273051,
                    'currency': 'usd',
                    'id': 'develtech_999',
                    'interval': 'month',
                    'interval_count': 1,
                    'livemode': False,
                    'metadata': {},
                    'name': 'Devel.tech 9.99',
                    'object': 'plan',
                    'statement_descriptor': None,
                    'trial_period_days': None
                },
                'quantity': 1
            }],
            'has_more': False,
            'object': 'list',
            'total_count': 1,
            'url': '/v1/subscription_items?subscription=sub_BwuTCVDt1Klbil'
        },
        'livemode': False,
        'metadata': {},
        'object': 'subscription',
        'plan': {
            'amount': 999,
            'created': 1513273051,
            'currency': 'usd',
            'id': 'develtech_999',
            'interval': 'month',
            'interval_count': 1,
            'livemode': False,
            'metadata': {},
            'name': 'Devel.tech 9.99',
            'object': 'plan',
            'statement_descriptor': None,
            'trial_period_days': None
        },
        'quantity': 1,
        'start': 1513273056,
        'status': 'active',
        'tax_percent': None,
        'trial_end': None,
        'trial_start': None
    }

    subscriptions = {
        'data': [subscription],
        'has_more': False,
        'object': 'list',
        'total_count': 1,
        'url': '/v1/customers/cus_Bwrbeyo88aaUYP/subscriptions'
    }

    customer = {
        'account_balance': 0,
        'created': 1513262366,
        'currency': 'usd',
        'default_source': 'card_1BYxtEEzushJqDoiJUQkSyER',
        'delinquent': False,
        'description': 'Test user',
        'discount': None,
        'email': 'tony@git-pull.com',
        'id': 'cus_Bwrbeyo88aaUYP',
        'livemode': False,
        'metadata': {},
        'object': 'customer',
        'shipping': None,
        'sources': {
            'data': [{
                'address_city': 'new york',
                'address_country': 'usa',
                'address_line1': 'McAllister St',
                'address_line1_check': 'pass',
                'address_line2': None,
                'address_state': 'ny',
                'address_zip': '10013',
                'address_zip_check': 'pass',
                'brand': 'Visa',
                'country': 'US',
                'customer': 'cus_Bwrbeyo88aaUYP',
                'cvc_check': 'pass',
                'dynamic_last4': None,
                'exp_month': 4,
                'exp_year': 2032,
                'fingerprint': 'ZX4L088dUFClwtPD',
                'funding': 'credit',
                'id': 'card_1BYxtEEzushJqDoiJUQkSyER',
                'last4': '4242',
                'metadata': {},
                'name': 'John Doe',
                'object': 'card',
                'tokenization_method': None
            }],
            'has_more': False,
            'object': 'list',
            'total_count': 1,
            'url': '/v1/customers/cus_Bwrbeyo88aaUYP/sources'
        },
        'subscriptions': subscriptions
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

    assert not customer_object.discount

    subscriptions_url = customer_url + '/subscriptions'
    subscriptions_json = json.dumps(subscriptions)
    responses.add(
        responses.GET,
        subscriptions_url,
        body=subscriptions_json,
        status=200,
        content_type='application/json',
    )

    subscription_url = stripe.api_base + '/v1/subscriptions/{}'.format(
        subscription['id'])
    subscription_json = json.dumps(subscription)
    responses.add(
        responses.GET,
        subscription_url,
        body=subscription_json,
        status=200,
        content_type='application/json',
    )

    subscription_object = stripe.Subscription.retrieve(subscription['id'])
    assert hasattr(subscription_object, 'discount')

    for stripe_object in customer_object.subscriptions.auto_paging_iter():
        assert stripe_object.discount.coupon
        s = Discount.from_stripe_object(stripe_object.discount)
        assert isinstance(s, Discount)
