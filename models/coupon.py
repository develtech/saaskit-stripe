# -*- coding: utf-8 -*-
# flake8: NOQA: F401
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES


COUPON_DURATION_CHOICES = (
    ('FOREVER', 'forever'),
    ('ONCE', 'once'),
    ('REPREATING', 'repeating'),
)


class Coupon(models.Model):

    """Stipe Coupon object.

    A coupon contains information about a percent-off or amount-off discount
    you might want to apply to a customer. Coupons only apply to invoices; they
    do not apply to one-off charges.
    """

    livemode = models.BooleanField()
    created = models.DateTimeField()
    duration = models.CharField(
        max_length=255,
        choices=COUPON_DURATION_CHOICES,
        help_text=_(
            'One of ``forever``, ``once``, and ``repeating``. Describes how '
            'long a customer who applies this coupon will get the discount.'
        )
    )
    amount_off = models.PositiveIntegerField(
        help_text=_(
            'Amount (in the ``currency`` specified) that will be taken off '
            'the subtotal of any invoices for this customer.'
        )
    )
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_(
            'If ``amount_off`` has been set, the currency of the amount to '
            'take off.'
        )
    )
    duration_in_months = models.PositiveIntegerField(
        help_text=_(
            'If ``duration`` is ``repeating``, the number of months the '
            'coupon applies. Null if coupon ``duration`` is ``forever``'
            'or ``once``.'
        )
    )
    max_redemptions = models.PositiveIntegerField(
        help_text=_(
            'Maximum number of times this coupon can be redeemed, in total, '
            'before it is no longer valid.'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'coupon in a structured format.'
        )
    )
    percent_off = models.PositiveIntegerField(
        help_text=_(
            'Percent that will be taken off the subtotal of any invoices for '
            'this customer for the duration of the coupon. For example, a '
            'coupon with percent_off of 50 will make a $100 invoice $50 '
            'instead.'
        )
    )
    redeem_by = models.DateTimeField(
        help_text=_(
            'Date after which the coupon can no longer be redeemed'
        )
    )
    times_redeemed = models.PositiveIntegerField(
        help_text=_(
            'Number of times this coupon has been applied to a customer.'
        )
    )
    valid = models.BooleanField(
        help_text=_(
            'Taking account of the above properties, whether this coupon can '
            'still be applied to a customer'
        )
    )
