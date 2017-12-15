# -*- coding: utf-8 -*-
import pytest

from ..models import Source
from ..test import skip_if_stripe_mock_server_offline
import responses
import json


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_source_model_mock(mock_stripe):
    stripe_object = mock_stripe.Source.retrieve('test_hi')
    s = Source.from_stripe_object(stripe_object)
    assert isinstance(s, Source)


@responses.activate
def test_bank_and_card_sources(stripe):
    bank_account = {
        'account': 'acct_1032D82eZvKYlo2C',
        'account_holder_name': 'Jane Austen',
        'account_holder_type': 'individual',
        'bank_name': 'STRIPE TEST BANK',
        'country': 'US',
        'currency': 'usd',
        'fingerprint': '1JWtPxqbdX5Gamtc',
        'id': 'ba_1B3xSU2eZvKYlo2CDAgYCVfe',
        'last4': '6789',
        'metadata': {},
        'object': 'bank_account',
        'routing_number': '110000000',
        'status': 'new'
    }

    sources = {
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
            'tokenization_method': None}, bank_account],
        'has_more': False,
        'object': 'list',
        'url': '/v1/customers/cus_Bwrbeyo88aaUYP/sources'
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
        'sources': sources,
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

    customer = stripe.Customer.retrieve(customer_id)

    assert customer.id == customer_id
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == customer_url
    assert responses.calls[0].response.text == customer_json
