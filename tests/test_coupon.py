# -*- coding: utf-8 -*-
import pytest

from ..models import Coupon
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_coupon_model_mock(mock_stripe):
    coupon_list = mock_stripe.Coupon.list()
    assert len(coupon_list.data)
    for stripe_object in coupon_list.auto_paging_iter():
        s = Coupon.from_stripe_object(stripe_object)
        assert isinstance(s, Coupon)
