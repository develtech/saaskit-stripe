# -*- coding: utf-8 -*-
import stripe


def get_mock_stripe_client():
    stripe.api_base = 'http://localhost:12111'
    stripe.api_key = 'sk_test_...'
    return stripe
