# -*- coding: utf-8 -*-

from django.db import models

from django_extensions.db.fields import json


class Customer(models.Model):
    livemode = models.BooleanField(default=True)
    created = models.DateTimeField()
    account_balance = models.IntegerField()
    currency = models.CharField(max_length=255)
    default_source = models.CharField(max_length=255)
    delinquent = models.BooleanField()
    description = models.CharField(max_length=255)
    # discount = models.ForeignKey(Discount)
    email = models.EmailField()
    metadata = json.JSONField()
    sources = json.JSONField()
    # subscriptions = models.ManyToManyField(Subscription)
