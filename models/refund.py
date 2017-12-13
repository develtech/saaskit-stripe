# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json


REFUND_CHOICES = (
    ('duplicate', _('Duplicate')),
    ('fraudulent', _('Fraudulent')),
    ('requested_by_customer', _('Requested by customer')),
)


class Refund(models.Model):

    """Stripe Refund objects.

    Refund objects allow you to refund a charge that has previously been
    created but not yet refunded. Funds will be refunded to the credit or debit
    card that was originally charged. The fees you were originally charged are
    also refunded.
    """

    amount = models.IntegerField(
        help_text=_(
            'Amount reversed, in cents.'
        )
    )
    created = models.DateTimeField()
    currency = models.IntegerField(
        help_text=_(
            'Three-letter ISO code representing the currency of the reversal.'
        )
    )
    balance_transaction = models.CharField(
        max_length=255,
        help_text=_(
            'Balance transaction that describes the impact of this reversal '
            'on your account balance.'
        )
    )
    charge = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the charge that was '
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'It can be useful for storing additional information about the '
            'refund in a structured format.'
        )
    )
    reason = models.CharField(
        max_length=255,
        choices=REFUND_CHOICES,
        help_text=_(
            'Reason for the refund. If set, possible values are duplicate, '
            'fraudulent, and requested_by_customer.'
        )
    )
    receipt_number = models.CharField(
        max_length=255,
        help_text=_(
            'This is the transaction number that appears on email receipts '
            'sent for this refund.'
        )
    )
    description = models.CharField(max_length=255)
