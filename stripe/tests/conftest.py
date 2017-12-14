# -*- coding: utf-8 -*-
import pytest

from ..test import get_test_stripe_client


@pytest.fixture
def stripe():
    return get_test_stripe_client()


@pytest.fixture
def mock_stripe(stripe, request):
    """Set up a mock stripe client"""
    old_base = stripe.api_base
    stripe.api_base = 'http://localhost:12111'

    def resource_a_teardown():
        stripe.api_base = old_base

    request.addfinalizer(resource_a_teardown)

    return stripe
