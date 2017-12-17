# -*- coding: utf-8 -*-
import pytest

from ..models import SubscriptionItem
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_subscription_item_model_mock(mock_stripe):
    subscription_list = mock_stripe.SubscriptionItem.list()
    assert len(subscription_list.data)
    for stripe_object in subscription_list.auto_paging_iter():
        s = SubscriptionItem.from_stripe_object(stripe_object)
        assert isinstance(s, SubscriptionItem)
