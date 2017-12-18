# -*- coding: utf-8 -*-
import json

import pytest

import responses
import stripe

from ..models import Token
from ..test import skip_if_stripe_mock_server_offline


@responses.activate
@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_token_model_mock(mock_stripe):

    token = {
        'card': {
            'address_city': 'new york',
            'address_country': 'usa',
            'address_line1': '1003 humphrey st',
            'address_line1_check': 'unchecked',
            'address_line2': None,
            'address_state': 'NY',
            'address_zip': '10013',
            'address_zip_check': 'unchecked',
            'brand': 'Visa',
            'country': 'US',
            'cvc_check': 'unchecked',
            'dynamic_last4': None,
            'exp_month': 12,
            'exp_year': 2018,
            'fingerprint': 'ZX4L088dUFClwtPD',
            'funding': 'credit',
            'id': 'card_1BaVqoEzushJqDoidRjs68XP',
            'last4': '4242',
            'metadata': {},
            'name': 'John Doe',
            'object': 'card',
            'tokenization_method': None
        },
        'client_ip': '52.98.131.37',
        'created': 1513631323,
        'id': 'tok_1BaVqpEzushJqDoiMx84wxFG',
        'livemode': False,
        'object': 'token',
        'type': 'card',
        'used': False
    }

    token_id = token['id']
    token_url = stripe.api_base + '/v1/tokens/%s' % token_id
    token_json = json.dumps(token)
    responses.add(
        responses.GET,
        token_url,
        body=token_json,
        status=200,
        content_type='application/json',
    )

    stripe_object = mock_stripe.Token.retrieve(token_id)

    e = Token.from_stripe_object(stripe_object)
    assert isinstance(e, Token)
