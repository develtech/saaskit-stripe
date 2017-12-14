# -*- coding: utf-8 -*-
import pytest

from ..test import get_test_stripe_client


@pytest.fixture
def stripe():
    return get_test_stripe_client()
