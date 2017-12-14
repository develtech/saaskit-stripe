"""Test the helpers for the unittests."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import responses

from ..test import open_test_file


@responses.activate
def test_my_api(stripe):
    """Tests to assure the Stripe library is using the Requests library as an
    HTTP Client and responses is mocking the responses as intended."""

    body_json = open_test_file('customer/object.json').read()

    customer_id = json.loads(body_json)['id']
    customer_url = stripe.api_base + '/v1/customers/%s' % customer_id
    responses.add(
        responses.GET,
        customer_url,
        body=body_json,
        status=200,
        content_type='application/json',
    )

    customer = stripe.Customer.retrieve(customer_id)

    assert customer.id == customer_id
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == customer_url
    assert responses.calls[0].response.text == body_json
