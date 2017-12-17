# -*- coding: utf-8 -*-
import pytest

from ..models import Charge
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_charge_model_mock(mock_stripe):
    assert len(mock_stripe.Charge.list().data)
    for charge_object in mock_stripe.Charge.list().auto_paging_iter():
        c = Charge.from_stripe_object(charge_object)
        assert isinstance(c, Charge)
