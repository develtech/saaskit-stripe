# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


from django_extensions.db.fields import json


STATUS_CHOICES = (
    ("SUCCEEDED", "succeeded"),
    ("FAILED", "failed"),
)

class Charge(models.Model):
    livemode = models.BooleanField(default=True)
    amount = models.IntegerField()
    captured = models.BooleanField()
    created = models.DateTimeField()
    currency = models.CharField(max_length=255)  # todo ISO 3char fields
    paid = models.BooleanField()
    refunded = models.BooleanField()
    refunds = models.ManyToManyField("Refund")
    source = json.JSONField()
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    amount_refunded = models.PositiveIntegerField()
    balance_transaction = models.CharField(max_length=255)  # relation todo
    customer = models.ForeignKey("Customer")
    description = models.CharField(max_length=255)
    dispute = models.ForeignKey("Dispute", blank=True, null=True)
    failure_code = models.CharField(max_length=255)
    failure_message = models.CharField(max_length=255)
    invoice = models.ForeignKey("Invoice")
    metadata = json.JSONField()
    receipt_email = models.EmailField()
    receipt_number = models.CharField(max_length=255)
    application_fee = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    fraud_details= json.JSONField()
    shipping = json.JSONField()
    transfer = models.CharField(max_length=255)

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
    discount = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    discount = models.ForeignKey('Discount')
    email = models.EmailField()
    metadata = json.JSONField()
    sources = json.JSONField()
    subscriptions = models.ForeignKey("Subscription")


BRAND_CHOICES = (
    ("VISA", "Visa"),
    ("AMERICAN_EXPRESS", "American Express"),
    ("MASTERCARD", "MasterCard"),
    ("DISCOVER", "Discover"),
    ("JCB", "JCB"),
    ("DINERS_CLUB", "Diners Club"),
    ("UNKNOWN", "Unknown"),
)

class Card(models.Model):
    brand = models.CharField(choices=BRAND_CHOICES, max_length=255)

class Subscription(models.Model):
    pass

class Plan(models.Model):
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
