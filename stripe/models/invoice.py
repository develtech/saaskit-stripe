# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES


class Invoice(models.Model):

    """Stripe Invoice object.

    Invoices are statements of what a customer owes for a particular billing
    period, including subscriptions, invoice items, and any automatic proration
    adjustments if necessary.

    Once an invoice is created, payment is automatically attempted. Note that
    the payment, while automatic, does not happen exactly at the time of
    invoice creation. If you have configured webhooks, the invoice will wait
    until one hour after the last webhook is successfully sent (or the last
    webhook times out after failing).

    Any customer credit on the account is applied before determining how much
    is due for that invoice (the amount that will be actually charged). If the
    amount due for the invoice is less than 50 cents (the minimum for a
    charge), We add the amount to the customer's running account balance to be
    added to the next invoice. If this amount is negative, it will act as a
    credit to offset the next invoice. Note that the customer account balance
    does not include unpaid invoices; it only includes balances that need to be
    taken into account when calculating the amount due for the next invoice.
    """

    livemode = models.BooleanField()
    amount_due = models.IntegerField(
        help_text=_(
            'Final amount due at this time for this invoice. If the invoice’s '
            'total is smaller than the minimum charge amount, for example, or '
            'if there is account credit that can be applied to the invoice, '
            'the ``amount_due`` may be 0. If there is a positive '
            '``starting_balance`` for the invoice (the customer owes money), '
            'the amount_due will also take that into account. The charge that '
            'gets generated for the invoice will be for the amount specified '
            'in amount_due.',
        ),
    )
    attempt_count = models.PositiveIntegerField(
        help_text=_(
            'Number of payment attempts made for this invoice, from the '
            'perspective of the payment retry schedule. Any payment attempt '
            'counts as the first attempt, and subsequently only automatic '
            'retries increment the attempt count. In other words, manual '
            'payment attempts after the first attempt do not affect the '
            'retry schedule.',
        ),
    )
    attempted = models.BooleanField(
        help_text=_(
            'Whether or not an attempt has been made to pay the invoice. An '
            'invoice is not attempted until 1 hour after the '
            '``invoice.created`` webhook, for example, so you might not want '
            'to display that invoice as unpaid to your users.',
        ),
    )
    closed = models.BooleanField(
        help_text=_(
            'Whether or not the invoice is still trying to collect payment. '
            'An invoice is closed if it’s either paid or it has been marked '
            'closed. A closed invoice will no longer attempt to collect '
            'payment.',
        ),
    )
    currency = models.CharField(max_length=255, choices=CURRENCY_CHOICES)
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()
    forgiven = models.BooleanField(
        help_text=_(
            'Whether or not the invoice has been forgiven. Forgiving an '
            'invoice instructs us to update the subscription status as if the '
            'invoice were succcessfully paid. Once an invoice has been '
            'forgiven, it cannot be unforgiven or reopened',
        ),
    )
    lines = json.JSONField(
        help_text=_(
            'The individual line items that make up the invoice. ``lines`` is '
            'sorted as follows: invoice items in reverse chronological order, '
            'followed by the subscription, if any.',
        ),
    )
    paid = models.BooleanField(
        help_text=_(
            'Whether or not payment was successfully collected for this '
            'invoice. An invoice can be paid (most commonly) with a charge or '
            'with credit from the customer’s account balance.',
        ),
    )
    period_end = models.DateTimeField(
        help_text=_(
            'End of the usage period during which invoice items were added to '
            'this invoice',
        ),
    )
    period_start = models.DateTimeField(
        help_text=_(
            'Start of the usage period during which invoice items were added '
            'to this invoice',
        ),
    )
    starting_balance = models.IntegerField(
        help_text=_(
            'Starting customer balance before attempting to pay invoice. If '
            'the invoice has not been attempted yet, this will be the current '
            'customer balance.',
        ),
    )
    subtotal = models.IntegerField(
        help_text=_(
            'Total of all subscriptions, invoice items, and prorations on the '
            'invoice before any discount is applied',
        ),
    )
    total = models.IntegerField(help_text=_('Total after discount'))
    application_fee = models.IntegerField(
        help_text=_(
            'The fee in cents that will be applied to the invoice and '
            'transferred to the application owner’s Stripe account when the '
            'invoice is paid.',
        ),
    )

    # Reverse
    # charge = models.ForeignKey(
    #     'Charge',
    #     help_text=_(
    #         'ID of the latest charge generated for this invoice, if any.'
    #     )
    # )

    description = models.CharField(max_length=255)
    discount = models.ForeignKey(
        'Discount',
        on_delete=models.CASCADE,
    )
    ending_balance = models.IntegerField(
        help_text=_(
            'Ending customer balance after attempting to pay invoice. If the '
            'invoice has not been attempted yet, this will be null.',
        ),
    )
    next_payment_attempt = models.DateTimeField(
        help_text=_(
            'The time at which payment will next be attempted.',
        ),
    )
    receipt_number = models.CharField(
        max_length=255,
        help_text=_(
            'This is the transaction number that appears on email receipts '
            'sent for this invoice.',
        ),
    )
    statement_descriptor = models.CharField(
        max_length=255,
        help_text=_(
            'Extra information about an invoice for the customer’s credit '
            'card statement.',
        ),
    )
    subscription = models.ForeignKey(
        'Subscription',
        help_text=_(
            'The subscription that this invoice was prepared for, if any.',
        ),
        on_delete=models.CASCADE,
    )
    webhooks_delivered_at = models.DateTimeField(
        help_text=_(
            'The time at which webhooks for this invoice were successfully '
            'delivered (if the invoice had no webhooks to deliver, this will '
            'match ``date``). Invoice payment is delayed until webhooks are '
            'delivered, or until all webhook delivery attempts have been '
            'exhausted.',
        ),
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'invoice in a structured format.'))
    subscription_proration_date = models.IntegerField(
        help_text=_(
            'Only set for upcoming invoices that preview prorations. The time '
            'used to calculate prorations.',
        ),
    )
    tax = models.IntegerField(
        help_text=_(
            'The amount of tax included in the total, calculated from '
            '``tax_percent`` and the subtotal. If no ``tax_percent`` is '
            'defined, this value will be null.',
        ),
    )
    tax_percent = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text=_(
            'This percentage of the subtotal has been added to the total '
            'amount of the invoice, including invoice line items and '
            'discounts. This field is inherited from the subscription’s '
            '``tax_percent`` field, but can be changed before the invoice is '
            'paid. This field defaults to null.',
        ),
    )
