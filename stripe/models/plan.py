# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

import pytz
from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES

PLAN_INTERVAL_CHOICES = (
    ('day', _('Day')),
    ('week', _('Week')),
    ('month', _('Month')),
    ('year', _('Year')),
)


class Plan(models.Model):

    """Stripe Plan object.

    A subscription plan contains the pricing information for different products
    and feature levels on your site. For example, you might have a $10/month
    plan for basic features and a different $20/month plan for premium
    features.
    """
    id = models.CharField(max_length=255, primary_key=True)
    livemode = models.BooleanField()
    amount = models.PositiveIntegerField(
        help_text=_(
            'The amount in cents to be charged on the interval specified',
        ),
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_(
            'Currency in which the subscription will be charged',
        ),
    )
    interval = models.CharField(
        choices=PLAN_INTERVAL_CHOICES,
        max_length=255,
        help_text=_(
            'One of ``day``, ``week``, ``month`` or ``year``. The frequency '
            'with which a subscription should be billed.',
        ),
    )
    interval_count = models.PositiveIntegerField(
        help_text=_(
            'The number of intervals (specified in the ``interval`` property) '
            'between each subscription billing. For example, '
            '``interval=month`` and interval_count=3 bills every 3 months.',
        ),
    )
    name = models.CharField(
        max_length=255,
        help_text=_(
            'Display name of the plan',
        ),
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'plan in a structured format.',
        ),
    )
    trial_period_days = models.PositiveIntegerField(
        help_text=_(
            'Number of trial period days granted when subscribing a customer '
            'to this plan. Null if the plan has no trial period.',
        ),
        null=True,
    )
    statement_descriptor = models.CharField(
        max_length=255,
        help_text=_(
            'Extra information about a charge for the customer’s credit card '
            'statement.',
        ),
        null=True,
    )

    @staticmethod
    def from_stripe_object(stripe_object):
        _dict = stripe_object.to_dict()
        _dict.pop('object')

        for field in Plan._meta.get_fields():
            if isinstance(field, models.DateTimeField):
                _dict[field.name] = datetime.datetime.fromtimestamp(
                    int(_dict[field.name])).replace(tzinfo=pytz.utc)

        s = Plan(**_dict)
        s.save()
        return s
