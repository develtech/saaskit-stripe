# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES


class BalanceTransaction(models.Model):
    amount = models.IntegerField(
        help_text=_(
            'Gross amount of the transaction, in cents'
        )
    )
    available_on = models.DateTimeField(
        help_text=_(
            'The date the transaction’s net funds will become available in '
            'the Stripe balance.'
        )
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES
    )
    fee = models.IntegerField(
        help_text=_(
            'Fees (in cents) paid for this transaction'
        )
    )
    fee_details = json.JSONField(
        help_text=_(
            'Detailed breakdown of fees (in cents) paid for this transaction'
        )
    )
    net = models.IntegerField(
        help_text=_(
            'Net amount of the transaction, in cents.'
        )
    )
    status = models.CharField(
        max_length=255,
        help_text=_(
            'If the transaction’s net funds are available in the Stripe '
            'balance yet. Either ``available`` or ``pending``.'
        )
    )
    type = models.CharField(
        max_length=255,
        help_text=_(
            'Type of the transaction, one of: ``charge``, ``refund``, '
            '``adjustment``, ``application_fee``, ``application_fee_refund``, '
            '``transfer``, ``transfer_cancel`` or ``transfer_failure``.'
        )
    )
    description = models.CharField(max_length=255)
    source = json.JSONField(
        help_text=_(
            'The Stripe object this transaction is related to.'
        )
    )
    sourced_transfers = json.JSONField(
        help_text=_(
            'The transfers (if any) for which source is a source_transaction.'
        )
    )
