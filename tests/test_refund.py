# -*- coding: utf-8 -*-
import pytest

from ..models import Refund
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_plan_model_mock(mock_stripe):
    refund_list = mock_stripe.Refund.list()
    assert len(refund_list.data)
    for stripe_object in refund_list.auto_paging_iter():
        e = Refund.from_stripe_object(stripe_object)
        assert isinstance(e, Refund)
