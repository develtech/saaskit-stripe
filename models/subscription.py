# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

SUBSCRIPTION_STATUS_CHOICES = (
    ('trialing', _('Trialing')),
    ('active', _('Active')),
    ('past_due', _('Past due')),
    ('canceled', _('Canceled')),
    ('unpaid', _('Unpaid')),
)


class Subscription(models.Model):

    """Stripe subscription object.

    Subscriptions allow you to charge a customer's card on a recurring basis. A
    subscription ties a customer to a particular plan `you've created`_.

    .. _you've created: https://stripe.com/docs/api#create_plan
    """

    cancel_at_period_end = models.BooleanField(
        help_text=_(
            'If the subscription has been canceled with the ``at_period_end``'
            'flag set to ``true``, ``cancel_at_period_end`` on the '
            'subscription will be true. You can use this attribute to '
            'determine whether a subscription that has a status of active is '
            'scheduled to be canceled at the end of the current period.',
        ),
    )
    customer = models.ForeignKey(
        'Customer',
        on_delete=models.CASCADE,
    )
    plan = models.ForeignKey(
        'Plan',
        help_text=_(
            'Hash describing the plan the customer is subscribed to',
        ),
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()
    start = models.DateTimeField(help_text=_('Date the subscription started',),)
    status = models.CharField(
        max_length=255,
        choices=SUBSCRIPTION_STATUS_CHOICES,
        help_text=_(
            'Possible values are ``trialing``, ``active``, ``past_due``, '
            '``canceled``, or ``unpaid``. A subscription still in its trial '
            'period is ``trialing`` and moves to ``active`` when the trial '
            'period is over. When payment to renew the subscription fails, '
            'the subscription becomes ``past_due``. After Stripe has '
            'exhausted all payment retry attempts, the subscription ends up '
            'with a status of either ``canceled`` or ``unpaid`` depending on '
            'your retry settings. Note that when a subscription has a status '
            'of ``unpaid``, no subsequent invoices will be attempted '
            '(invoices will be created, but then immediately automatically '
            'closed. Additionally, updating customer card details will not '
            'lead to Stripe retrying the latest invoice.). After receiving '
            'updated card details from a customer, you may choose to reopen '
            'and pay their closed invoices.',
        ),
    )
    application_fee_percent = models.CharField(
        max_length=255,
        help_text=_(
            'A positive decimal that represents the fee percentage of the '
            'subscription invoice amount that will be transferred to the '
            'application owner’s Stripe account each billing period.',
        ),
    )
    canceled_at = models.DateTimeField(
        help_text=_(
            'If the subscription has been canceled, the date of that '
            'cancellation. If the subscription was canceled with '
            '``cancel_at_period_end``, canceled_at will still reflect the '
            'date of the initial cancellation request, not the end of the '
            'subscription period when the subscription is automatically moved '
            'to a canceled state.',
        ),
    )
    current_period_start = models.DateTimeField(
        help_text=_(
            'End of the current period that the subscription has been '
            'invoiced for. At the end of this period, a new invoice will be '
            'created.',
        ),
    )
    discount = models.ForeignKey(
        'Discount',
        help_text=_(
            'Describes the current discount applied to this subscription, if '
            'there is one. When billing, a discount applied to a subscription '
            'overrides a discount applied on a customer-wide basis.',
        ),
        on_delete=models.CASCADE,
    )
    ended_at = models.DateTimeField(
        help_text=_(
            'If the subscription has ended (either because it was canceled or '
            'because the customer was switched to a subscription to a new '
            'plan), the date the subscription ended',
        ),
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'subscription in a structured format.',
        ),
    )
    trial_end = models.DateTimeField(
        help_text=_(
            'If the subscription has a trial, the end of that trial.',
        ),
    )
    trial_start = models.DateTimeField(
        help_text=_(
            'If the subscription has a trial, the beginning of that trial.',
        ),
    )
    tax_percent = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text=_(
            'If provided, each invoice created by this subscription will '
            'apply the tax rate, increasing the amount billed to the customer.',
        ),
    )

    @staticmethod
    def from_stripe_object(stripe_object):
        _dict = stripe_object.to_dict()
        _dict.pop('object')
        _dict.pop('customer')

        return Subscription(**_dict)
