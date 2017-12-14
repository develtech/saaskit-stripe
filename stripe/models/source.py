# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

import pytz
from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES

FLOW_CHOICES = (
    ('redirect', _('redirect')),
    ('receiver', _('receiver')),
    ('code_verification', _('code verification')),
    ('none', _('none')),
)
SOURCE_STATUS_CHOICES = (
    ('canceled', _('Canceled')),
    ('chargeable', _('Chargeable')),
    ('failed', _('Failed')),
    ('pending', _('Pending')),
)
SOURCE_TYPE_CHOICES = (
    ('card', _('Card')),
    ('three_d_secure', _('3-D Secure')),
    ('giropay', _('Giropay')),
    ('sepa_debit', _('SEPA Debit')),
    ('ideal', _('IDEAL')),
    ('sofort', _('SOFORT')),
    ('bancontact', _('Bancontact')),
    ('alipay', _('Alipay')),
)
SOURCE_USAGE_CHOICES = (
    ('reusable', _('Reuseable')),
    ('single_use', _('Single-use')),
)


class Source(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    amount = models.PositiveIntegerField()
    client_string = models.CharField(max_length=255)
    code_verification = json.JSONField()
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_(
            'Currency in which the subscription will be charged',
        ),
    )
    flow = models.CharField(
        choices=FLOW_CHOICES,
        max_length=24,
    )
    livemode = models.BooleanField()
    metadata = json.JSONField()
    owner = json.JSONField()
    receiver = json.JSONField()
    redirect = json.JSONField()
    statement_descriptor = models.CharField(max_length=255,)
    status = models.CharField(
        max_length=255,
        choices=SOURCE_STATUS_CHOICES,
    )
    type = models.CharField(
        max_length=255,
        choices=SOURCE_TYPE_CHOICES,
    )
    usage = models.CharField(
        max_length=255,
        choices=SOURCE_USAGE_CHOICES,
    )
