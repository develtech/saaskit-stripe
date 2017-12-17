# -*- coding: utf-8 -*-
from django.db import models

from django_extensions.db.fields import json

from ..utils import UnixDateTimeField, get_customer_info
from .plan import Plan


class SubscriptionItem(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    created = UnixDateTimeField()
    plan = models.ForeignKey(
        'Plan',
        on_delete=models.CASCADE,
        null=True,
    )

    subscription = models.ForeignKey(
        'Subscription',
        on_delete=models.CASCADE,
        null=True,
    )
    metadata = json.JSONField()
    proration_date = UnixDateTimeField(null=True)
    prorate = models.BooleanField(null=True)
    quantity = models.IntegerField(null=True)

    @classmethod
    def from_stripe_object(cls, stripe_object, customer=None):
        _dict = stripe_object.to_dict()
        _dict.pop('object')

        _dict = get_customer_info(_dict, customer)

        if 'plan' in _dict:
            _dict['plan'] = Plan.from_stripe_object(_dict.pop('plan'))

        s = cls(**_dict)
        s.save()
        return s
