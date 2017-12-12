# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES


class ApplicationFeeRefund(models.Model):

    """Stripe Application Fee Refund object.

    Application Fee Refund objects allow you to refund an application fee that
    has previously been created but not yet refunded. Funds will be refunded to
    the Stripe account that the fee was originally collected from.
    """

    amount = models.IntegerField(
        help_text=_('Amount reversed, in cents.')
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'Three-letter ISO currency code representing the currency of the '
            'reverse.'
        ),
        choices=CURRENCY_CHOICES
    )
    balance_transaction = models.ForeignKey(
        'BalanceTransaction',
        help_text=_(
            'Balance transaction that describes the impact of this reversal '
            'on your account balance.'
        ),
        on_delete=models.CASCADE,
    )
    fee = models.ForeignKey(
        'ApplicationFee',
        help_text=_(
            'ID of the application fee that was refunded.'
        ),
        on_delete=models.CASCADE,
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'charge in a structured format.'
        )
    )
