# -*- coding: utf-8 -*-
import pytest

from ..models import Source
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_source_model_mock(mock_stripe):
    stripe_object = mock_stripe.Source.retrieve('test_hi')
    s = Source.from_stripe_object(stripe_object)
    assert isinstance(s, Source)
