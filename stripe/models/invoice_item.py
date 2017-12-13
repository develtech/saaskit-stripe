# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES


class InvoiceItem(models.Model):

    """Stripe Invoice Item object.

    Sometimes you want to add a charge or credit to a customer but only
    actually charge the customer's card at the end of a regular billing
    cycle. This is useful for combining several charges to minimize
    per-transaction fees or having Stripe tabulate your usage-based
    billing totals.
    """

    livemode = models.BooleanField()
    amount = models.IntegerField()
    currency = models.CharField(max_length=255, choices=CURRENCY_CHOICES)
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    discountable = models.BooleanField(
        help_text=_(
            'If true, discounts will apply to this invoice item. Always false '
            'for prorations.',
        ),
    )
    proration = models.BooleanField(
        help_text=_(
            'Whether or not the invoice item was created automatically as a '
            'proration adjustment when the customer switched plans',
        ),
    )
    description = models.CharField(max_length=255)
    invoice = models.CharField(max_length=255)
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'invoice item in a structured format.',
        ),
    )
    period = json.JSONField()
    plan = models.ForeignKey(
        'Plan',
        help_text=_(
            'If the invoice item is a proration, the plan of the subscription '
            'that the proration was computed for.',
        ),
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        help_text=_(
            'If the invoice item is a proration, the quantity of the '
            'subscription that the proration was computed for.',
        ),
    )
    subscription = models.ForeignKey(
        'Subscription',
        help_text=_(
            'The subscription that this invoice item has been created for, if '
            'any.',
        ),
        on_delete=models.CASCADE,
    )
