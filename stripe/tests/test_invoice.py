# -*- coding: utf-8 -*-
import pytest

from ..models import Invoice
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_invoice_model_mock(mock_stripe):
    assert len(mock_stripe.Invoice.list().data)
    for stripe_object in mock_stripe.Invoice.list().auto_paging_iter():
        c = Invoice.from_stripe_object(stripe_object)
        assert isinstance(c, Invoice)
