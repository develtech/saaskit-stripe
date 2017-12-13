# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json


class Balance(models.Model):

    """Stripe Balance object.

    This is an object representing your Stripe balance. You can retrieve it to
    see the balance currently on your Stripe account.

    You can also retrieve a list of the balance history, which contains a full
    list of transactions that have ever contributed to the balance (charges,
    refunds, transfers, and so on).
    """

    livemode = models.BooleanField()
    available = json.JSONField(
        help_text=_(
            'Funds that are available to be paid out automatically by '
            'Stripe or explicitly via the transfers API.',
        ),
    )
    pending = json.JSONField(
        help_text=_(
            'Funds that are not available in the balance yet, due to the '
            '7-day rolling pay cycle.',
        ),
    )
