# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


from django_extensions.db.fields import json


class Charge(models.Model):
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


class Refund(models.Model):
    amount = models.IntegerField()
    created = models.DateTimeField()
    currency = models.IntegerField()
    balance_transaction = models.CharField(max_length=255)
    charge = models.CharField(max_length=255)
    metadata = json.JSONField()
    reason = models.CharField(max_length=255)
    receipt_number = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Customer(models.Model):
    livemode = models.BooleanField()
    created = models.DateTimeField()
    account_balance = models.DateTimeField()
    currency = models.CharField(max_length=255)
    default_source = models.CharField(max_length=255)
    delinquent = models.CharField(max_length=255)

class Card(models.Model):
    pass

class Discount(models.Model):
    pass

class Invoice(models.Model):
    pass

class InvoiceItem(models.Model):
    pass

class Dispute(models.Model):
    pass

class Transfer(models.Model):
    pass

class TransferReversal(models.Model):
    pass

class Recipient(models.Model):
    pass

class ApplicationFee(models.Model):
    pass

class ApplicationFeeRefund(models.Model):
    pass

class Account(models.Model):
    pass

class Balance(models.Model):
    pass

class Event(models.Model):
    pass

class Token(models.Model):
    pass

class BitCoinReceiver(models.Model):
    pass
