# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES

TRANSFER_STATUS_CHOICES = (
    ('paid', _('Paid')),
    ('canceled', _('Canceled')),
    ('failed', _('Failed')),
)
TRANSFER_TYPE_CHOICES = (
    ('card', _('Card')),
    ('bank_account', _('Bank account')),
    ('stripe_account', _('Stripe account')),
)
TRANSFER_FAILURE_CHOICES = (
    (
        'insufficient_funds', _(
            'Your Stripe account has insufficient funds to cover the transfer.'
        )
    ),
    (
        'account_closed',
        _(
            'The bank account has been closed.'
        )
    ),
    (
        'no_account',
        _(
            'The bank account details on file are probably incorrect. No bank '
            'account could be located with those details.'
        )
    ),
    (
        'invalid_account_number',
        _(
            'The routing number seems correct, but the account number is '
            'invalid.'
        )
    ),
    (
        'debit_not_authorized',
        _(
            'Debit transactions are not approved on the bank account. Stripe '
            'requires bank accounts to be set up for both credit and debit '
            'transfers.'
        )
    ),
    (
        'bank_ownership_changed',
        _(
            'The destination bank account is no longer valid because its '
            'branch has changed ownership.'
        )
    ),
    (
        'account_frozen',
        _('The bank account has been frozen.')
    ),
    (
        'could_not_process',
        _('The bank could not process this transfer.')
    ),
    (
        'bank_account_restricted',
        _(
            'The bank account has restrictions on either the type or number '
            'of transfers allowed. This normally indicates that the bank '
            'account is a savings or other non-checking account.'
        )
    ),
    (
        'invalid_currency',
        _(
            'The bank was unable to process this transfer because of its '
            'currency. This is probably because the bank account cannot '
            'accept payments in that currency.'
        )
    ),
)


class Transfer(models.Model):

    """Stripe Transfer object.

    When Stripe sends you money or you initiate a transfer to a bank account,
    debit card, or connected Stripe account, a transfer object will be created.
    You can retrieve individual transfers as well as list all transfers.

    View the `documentation` on creating transfers via the API.

    .. _documentation: https://stripe.com/docs/tutorials/sending-transfers
    """

    livemode = models.BooleanField()
    amount = models.IntegerField(
        help_text=_(
            'Amount (in cents) to be transferred to your bank account'
        )
    )
    created = models.DateTimeField(
        help_text=_(
            'Time that this record of the transfer was first created.'
        )
    )
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_(
            'Three-letter ISO code representing the currency of the transfer.'
        )
    )
    date = models.DateTimeField(
        help_text=_(
            'Date the transfer is scheduled to arrive in the bank. This '
            'doesn’t factor in delays like weekends or bank holidays.'
        )
    )
    reversals = json.JSONField(
        help_text=_(
            'A list of reversals that have been applied to the transfer.'
        )
    )
    reversed = models.BooleanField(
        help_text=_(
            'Whether or not the transfer has been fully reversed. If the '
            'transfer is only partially reversed, this attribute will still '
            'be false.'
        )
    )

    status = models.CharField(
        max_length=255,
        help_text=_(
            'Current status of the transfer (``paid``, ``pending``, '
            '``canceled`` or ``failed``). A transfer will be ``pending`` '
            'until it is submitted, at which point it becomes ``paid``. If it '
            'does not go through successfully, its status will change to '
            '``failed`` or ``canceled``.'
        ),
        choices=TRANSFER_STATUS_CHOICES
    )
    type = models.CharField(
        max_length=255,
        help_text=_(
            'The type of this type of this transfer. Can be ``card``, '
            '``bank_account``, or ``stripe_account``.'
        ),
        choices=TRANSFER_TYPE_CHOICES
    )
    amount_reversed = models.IntegerField(
        help_text=_(
            'Amount in cents reversed (can be less than the amount attribute '
            'on the transfer if a partial reversal was issued).'
        )
    )
    balance_transaction = models.ForeignKey(
        'BalanceTransaction',
        help_text=_(
            'Balance transaction that describes the impact of this transfer '
            'on your account balance.',
        ),
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        help_text=_(
            'Internal-only description of the transfer'
        )
    )
    failure_code = models.CharField(
        max_length=255,
        help_text=_(
            'Error code explaining reason for transfer failure if available. '
            'See Types of transfer failures for a list of failure codes.'
        ),
        choices=TRANSFER_FAILURE_CHOICES
    )
    failure_message = models.TextField(
        help_text=_(
            'Message to user further explaining reason for transfer failure '
            'if available.'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'transfer in a structured format.'
        )
    )
    application_fee = models.CharField(max_length=255)
    destination = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the bank account, card, or Stripe account the transfer was '
            'sent to.'
        )
    )
    destination_payment = models.CharField(
        max_length=255,
        help_text=_(
            'If the destination is a Stripe account, this will be the ID of '
            'the payment that the destination account received for the '
            'transfer.'
        )
    )
    source_transaction = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the charge (or other transaction) that was used to fund '
            'the transfer. If null, the transfer was funded from the '
            'available balance.'
        )
    )
    statement_descriptor = models.CharField(
        max_length=255,
        help_text=_(
            'Extra information about a transfer to be displayed on the user’s '
            'bank statement.'
        )
    )
