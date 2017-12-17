# -*- coding: utf-8 -*-
import pytest

from ..models import InvoiceItem
from ..test import skip_if_stripe_mock_server_offline


@skip_if_stripe_mock_server_offline
@pytest.mark.django_db(transaction=True)
def test_invoice_item_model_mock(mock_stripe):
    invoice_items = mock_stripe.InvoiceItem.list()
    assert len(invoice_items.data)
    for stripe_object in invoice_items.auto_paging_iter():
        c = InvoiceItem.from_stripe_object(stripe_object)
        assert isinstance(c, InvoiceItem)
