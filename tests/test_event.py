# -*- coding: utf-8 -*-
import pytest

from ..models import Event
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_plan_model_mock(mock_stripe):
    event_list = mock_stripe.Event.list()
    assert len(event_list.data)
    for stripe_object in event_list.auto_paging_iter():
        e = Event.from_stripe_object(stripe_object)
        assert isinstance(e, Event)
