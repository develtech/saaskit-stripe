# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES


class TransferReversal(models.Model):

    """Stripe Transfer Reversal object.

    A previously created transfer can be reversed if it has not yet been paid
    out. Funds will be refunded to your available balance, and the fees you
    were originally charged on the transfer will be refunded. You may not
    reverse automatic Stripe transfers.
    """

    amount = models.IntegerField(
        help_text=_(
            'Amount reversed, in cents.'
        )
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_(
            'Three-letter ISO code representing the currency of the reversal.'
        )
    )
    balance_transaction = models.ForeignKey(
        'BalanceTransaction',
        help_text=_(
            'Balance transaction that describes the impact of this reversal '
            'on your account balance.'
        ),
        related_name='transfer_reversal_balance_transaction',
        on_delete=models.CASCADE,
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'transfer reversal in a structured format.'
        )
    )
    transfer = models.ForeignKey(
        'Transfer',
        help_text=_(
            'ID of the transfer that was reversed.'
        ),
        on_delete=models.CASCADE,
    )
