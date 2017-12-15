# -*- coding: utf-8 -*-
import pytest

from ..models import Plan
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_plan_model_mock(mock_stripe):
    assert len(mock_stripe.Plan.list().data)
    for plan_object in mock_stripe.Plan.list().auto_paging_iter():
        c = Plan.from_stripe_object(plan_object)
        assert isinstance(c, Plan)
