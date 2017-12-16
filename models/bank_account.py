# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES
from .payment_method import PaymentMethod

BANK_ACCOUNT_TYPES = (
    ('individual', _('Individual')),
    ('company', _('Company')),
)

BANK_ACCOUNT_STATUS = (
    ('new', _('New')),
    ('validated', _('Validated')),
    ('verified', _('Verified')),
    ('verification_failed', _('Verification Failed')),
    ('errored', _('Errored')),
)


class BankAccount(PaymentMethod):
    account = models.ForeignKey('account', on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=255)
    account_type = models.CharField(max_length=255, choices=BANK_ACCOUNT_TYPES)
    bank_name = models.CharField(max_length=255)
    currency = models.CharField(max_length=255, choices=CURRENCY_CHOICES)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    default_for_currency = models.BooleanField()
    fingerprint = models.CharField(max_length=255)
    last4 = models.CharField(max_length=4)
    metadata = json.JSONField()
    routing_number = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=BANK_ACCOUNT_STATUS)

    @classmethod
    def from_stripe_object(cls, stripe_object, customer):
        _dict = stripe_object.to_dict()
        _dict.pop('object')
        if 'customer' in _dict:
            _dict.pop('customer')
            _dict['customer'] = customer
        c = cls(**_dict)
        c.save()

        return c
