# -*- coding: utf-8 -*-
import pytest

from ..test import get_mock_stripe_client


@pytest.fixture
def stripe():
    return get_mock_stripe_client()
