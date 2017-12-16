# -*- coding: utf-8 -*-
"""
As of December 16th, 2017, Stripe breaks payment methods into 3 categories:

- Bank Accounts
- Cards
- Sources

They must be retrieved through the Stripe API customer object.

Of these, the strangest of them is source. They're not listable, and directly
query-able. Some sources aren't reuseable:
https://stripe.com/docs/sources#supported-payment-methods

"""

from django.db import models


class PaymentMethod(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
