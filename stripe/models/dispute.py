# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json


class Dispute(models.Model):

    """Stripe Dispute object.

    A dispute occurs when a customer questions your charge with their bank or
    credit card company. When a customer disputes your charge, you're given the
    opportunity to respond to the dispute with evidence that shows the charge
    is legitimate. You can find more information about the dispute process in
    our disputes FAQ.
    """

    livemode = models.BooleanField()
    amount = models.IntegerField(
        help_text=_(
            'Disputed amount. Usually the amount of the charge, but can '
            'differ (usually because of currency fluctuation or because only '
            'part of the order is disputed).'
        )
    )
    # reverse
    # charge = models.ForeignKey(
    #     'Charge',
    #     help_text=_('ID of the charge that was disputed')
    # )
    created = models.DateTimeField(
        help_text=_('Date dispute was opened')
    )
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'Three-letter ISO currency code representing the currency of the '
            'amount that was disputed. '
        )
    )
    reason = models.CharField(
        max_length=255,
        help_text=_(
            'Reason given by cardholder for dispute. Possible values are '
            '``duplicate``, ``fraudulent``, ``subscription_canceled``, '
            '``product_unacceptable``, ``product_not_received``, '
            '``unrecognized``, ``credit_not_processed``, ``general``. Read '
            'more about dispute reasons.'
        )
    )
    status = models.CharField(
        max_length=255,
        help_text=_(
            'Current status of dispute. Possible values are '
            '``warning_needs_response``, ``warning_under_review``, '
            '``warning_closed``, ``needs_response``, ``response_disabled``, '
            '``under_review``, ``charge_refunded``, ``won``, ``lost``.'
        )
    )
    balance_transaction = models.ManyToManyField(
        'BalanceTransaction',
        help_text=_(
            'List of zero, one, or two balance transactions that show funds '
            'withdrawn and reinstated to your Stripe account as a result of '
            'this dispute.'
        )
    )
    evidence = models.ForeignKey(
        'DisputeEvidence',
        help_text=_(
            'Evidence provided to respond to a dispute. Updating any field in '
            'the hash will submit all fields in the hash for review.',
        ),
        on_delete=models.CASCADE,
    )
    evidence_details = json.JSONField(
        help_text=_(
            'Information about the evidence submission.'
        )
    )
    is_charge_refundable = models.BooleanField(
        'If true, it is still possible to refund the disputed payment. Once '
        'the payment has been fully refunded, no further funds will be '
        'withdrawn from your Stripe account as a result of this dispute.'
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'dispute in a structured format.'
        )
    )
