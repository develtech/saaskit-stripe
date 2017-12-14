"""Test the helpers for the unittests."""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.test import TestCase

import responses
import stripe

from .helpers import open_test_file

stripe.api_key = 'sk_test_BQokikJOvBiI2HlWgH4olfQ2'


class TestResponsesStripeSanity(TestCase):

    """Tests to assure the Stripe library is using the Requests
    library as an HTTP Client and responses is mocking the
    responses as intended."""

    @responses.activate
    def test_my_api(self):
        body_json = open_test_file('customer/object.json').read()

        customer_id = json.loads(body_json)['id']
        customer_url = 'https://api.stripe.com/v1/customers/%s' % customer_id
        responses.add(
            responses.GET,
            customer_url,
            body=body_json,
            status=200,
            content_type='application/json',
        )

        customer = stripe.Customer.retrieve(customer_id)

        self.assertEquals(customer.id, customer_id)
        self.assertEquals(len(responses.calls), 1)
        self.assertEquals(responses.calls[0].request.url, customer_url)
        self.assertEquals(responses.calls[0].response.text, body_json)
