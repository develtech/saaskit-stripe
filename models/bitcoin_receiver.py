# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES


class BitCoinReceiver(models.Model):

    """Stripe Bitcoin Receiver object.

    A Bitcoin receiver wraps a Bitcoin address so that a customer can push a
    payment to you. This `guide`_ describes how to use receivers to create
    Bitcoin payments.

    .. _guide: https://stripe.com/docs/guides/bitcoin
    """

    livemode = models.BooleanField()
    active = models.BooleanField(
        help_text=_(
            'True when this bitcoin receiver has received a non-zero amount '
            'of bitcoin.',
        ),
    )
    amount = models.PositiveIntegerField(
        help_text=_(
            'The amount of currency that you are collecting as payment.',
        ),
    )
    amount_received = models.PositiveIntegerField(
        help_text=_(
            'The amount of currency to which bitcoin_amount_received has been '
            'converted.',
        ),
    )
    bitcoin_amount = models.PositiveIntegerField(
        help_text=_(
            'The amount of bitcoin that the customer should send to fill the '
            'receiver. The bitcoin_amount is denominated in Satoshi: there '
            'are 10^8 Satoshi in one bitcoin.',
        ),
    )
    bitcoin_amount_received = models.PositiveIntegerField(
        help_text=_(
            'The amount of bitcoin that has been sent by the customer to this '
            'receiver.',
        ),
    )
    bitcoin_uri = models.URLField(
        help_text=_(
            'This URI can be displayed to the customer as a clickable link '
            '(to activate their bitcoin client) or as a QR code (for mobile '
            'wallets).',
        ),
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'Three-letter ISO currency code representing the currency to '
            'which the bitcoin will be converted.',
        ),
        choices=CURRENCY_CHOICES,
    )
    filled = models.BooleanField(
        help_text=_(
            'This flag is initially false and updates to true when the '
            'customer sends the bitcoin_amount to this receiver.',
        ),
    )
    inbound_address = models.CharField(
        max_length=255,
        help_text=_(
            'A bitcoin address that is specific to this receiver. The '
            'customer can send bitcoin to this address to fill the receiver.',
        ),
    )
    transactions = json.JSONField(
        help_text=_(
            'A list with one entry for each time that the customer sent '
            'bitcoin to the receiver. Hidden when viewing the receiver with a '
            'publishable key.',
        ),
    )
    uncaptured_funds = models.BooleanField(
        help_text=_(
            'This receiver contains uncaptured funds that can be used for a '
            'payment or refunded.',
        ),
    )
    description = models.CharField(max_length=255)
    email = models.EmailField(
        help_text=_(
            'The customer’s email address, set by the API call that creates '
            'the receiver.',
        ),
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'charge in a structured format.',
        ),
    )
    payment = models.CharField(
        max_length=255,
        help_text=_(
            'The ID of the payment created from the receiver, if any. Hidden '
            'when viewing the receiver with a publishable key.',
        ),
    )
    refund_address = models.CharField(
        max_length=255,
        help_text=_(
            'The refund address for these bitcoin, if communicated by the '
            'customer.',
        ),
    )
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    )
