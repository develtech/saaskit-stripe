# -*- coding: utf-8 -*-
import json

import pytest

import responses

from ..models import Customer, Source
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_source_model_mock(mock_stripe):
    stripe_object = mock_stripe.Source.retrieve('test_hi')
    s = Source.from_stripe_object(stripe_object)
    assert isinstance(s, Source)


@responses.activate
@pytest.mark.django_db(transaction=True)
def test_bank_and_card_sources(stripe):
    account = {
        'id': 'acct_1032D82eZvKYlo2C',
        'object': 'account',
        'business_logo': None,
        'business_name': 'Stripe.com',
        'business_url': None,
        'charges_enabled': False,
        'country': 'US',
        'created': 1385798567,
        'debit_negative_balances': True,
        'decline_charge_on': {
            'avs_failure': True,
            'cvc_failure': False
        },
        'default_currency': 'usd',
        'details_submitted': False,
        'display_name': 'Stripe.com',
        'email': 'site@stripe.com',
        'external_accounts': {
            'object': 'list',
            'data': [],
            'has_more': False,
            'total_count': 0,
            'url': '/v1/accounts/acct_1032D82eZvKYlo2C/external_accounts'
        },
        'legal_entity': {
            'additional_owners': [],
            'address': {
                'city': None,
                'country': 'US',
                'line1': None,
                'line2': None,
                'postal_code': None,
                'state': None
            },
            'business_name': None,
            'business_tax_id_provided': False,
            'dob': {
                'day': None,
                'month': None,
                'year': None
            },
            'first_name': None,
            'last_name': None,
            'personal_address': {
                'city': None,
                'country': 'US',
                'line1': None,
                'line2': None,
                'postal_code': None,
                'state': None
            },
            'personal_id_number_provided': False,
            'ssn_last_4_provided': False,
            'type': None,
            'verification': {
                'details': None,
                'details_code': 'failed_other',
                'document': None,
                'status': 'unverified'
            }
        },
        'metadata': {},
        'payout_schedule': {
            'delay_days': 7,
            'interval': 'daily'
        },
        'payout_statement_descriptor': None,
        'payouts_enabled': False,
        'product_description': None,
        'statement_descriptor': '',
        'support_email': None,
        'support_phone': None,
        'timezone': 'US/Pacific',
        'tos_acceptance': {
            'date': None,
            'ip': None,
            'user_agent': None
        },
        'type': 'standard',
        'verification': {
            'disabled_reason': 'fields_needed',
            'due_by': None,
            'fields_needed': [
                'business_url', 'external_account', 'product_description',
                'support_phone', 'tos_acceptance.date', 'tos_acceptance.ip'
            ]
        }
    }

    account_id = account['id']
    account_url = stripe.api_base + '/v1/accounts/%s' % account_id
    account_json = json.dumps(account)
    responses.add(
        responses.GET,
        account_url,
        body=account_json,
        status=200,
        content_type='application/json',
    )

    bank_account = {
        'account': 'acct_1032D82eZvKYlo2C',
        'account_holder_name': 'Jane Austen',
        'account_holder_type': 'individual',
        'bank_name': 'STRIPE TEST BANK',
        'country': 'US',
        'currency': 'usd',
        'default_for_currency': False,
        'fingerprint': '1JWtPxqbdX5Gamtc',
        'id': 'ba_1B3xSU2eZvKYlo2CDAgYCVfe',
        'last4': '6789',
        'metadata': {},
        'object': 'bank_account',
        'routing_number': '110000000',
        'status': 'new'
    }

    card = {
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
    }

    sources = {
        'data': [card, bank_account],
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

    customer_object = stripe.Customer.retrieve(customer_id)

    assert customer_object.id == customer_id
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == customer_url
    assert responses.calls[0].response.text == customer_json

    source_url = '%s/sources' % customer_url
    source_json = json.dumps(sources)
    responses.add(
        responses.GET,
        source_url,
        body=source_json,
        status=200,
        content_type='application/json',
    )

    card_url = '%s/%s' % (source_url, card['id'])
    card_json = json.dumps(card)
    responses.add(
        responses.GET,
        card_url,
        body=card_json,
        status=200,
        content_type='application/json',
    )

    card_object = customer_object.sources.retrieve(
        'card_1BYxtEEzushJqDoiJUQkSyER',
    )

    assert card_object.id == card['id']

    c = Customer.from_stripe_object(customer_object)
