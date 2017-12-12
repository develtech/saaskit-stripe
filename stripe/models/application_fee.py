# -*- coding: utf-8 -*-
# flake8: NOQA: F401
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES


class ApplicationFee(models.Model):

    """Stripe Application Fee object.

    When you collect a transaction fee on top of a charge made for your user
    (using Stripe Connect), an application fee object is created in your
    account. You can list, retrieve, and refund application fees.

    For more information on collecting transaction fees, see our documentation.
    """

    livemode = models.BooleanField()
    account = models.ForeignKey(
        'Account',
        help_text=_(
            'ID of the Stripe account this fee was taken from.',
        ),
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        help_text=_(
            'Amount earned, in cents.'
        )
    )
    application = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the Connect Application that earned the fee.'
        )
    )
    balance_transaction = models.ForeignKey(
        'BalanceTransaction',
        help_text=_(
            'Balance transaction that describes the impact of this collected '
            'application fee on your account balance (not including refunds).'
        ),
        on_delete=models.CASCADE,
    )
    charge = models.ForeignKey(
        'Charge',
        help_text=_(
            'ID of the charge that the application fee was taken from.'
        ),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'Three-letter ISO currency code representing the currency of the'
            'charge.'
        ),
        choices=CURRENCY_CHOICES
    )
    refunded = models.BooleanField(
        help_text=_(
            'Whether or not the fee has been fully refunded. If the fee is '
            'only partially refunded, this attribute will still be false.'
        )
    )
    # refunds reverse relation from 'Refund'
    amount_refunded = models.PositiveIntegerField()
