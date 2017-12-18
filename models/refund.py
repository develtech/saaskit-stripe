# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

import stripe
from django_extensions.db.fields import json

from ..utils import UnixDateTimeField

REFUND_CHOICES = (
    ('duplicate', _('Duplicate')),
    ('fraudulent', _('Fraudulent')),
    ('requested_by_customer', _('Requested by customer')),
)

REFUND_STATUS_CHOICES = (
    ('succeeded', _('Succeeded')),
    ('failed', _('Failed')),
    ('pending', _('Pending')),
    ('cancelled', _('Cancelled')),
)


class Refund(models.Model):

    """Stripe Refund objects.

    Refund objects allow you to refund a charge that has previously been
    created but not yet refunded. Funds will be refunded to the credit or debit
    card that was originally charged. The fees you were originally charged are
    also refunded.
    """
    id = models.CharField(max_length=255, primary_key=True)
    amount = models.IntegerField(help_text=_('Amount reversed, in cents.'))
    created = UnixDateTimeField()
    currency = models.CharField(
        max_length=3,
        help_text=_(
            'Three-letter ISO code representing the currency of the reversal.',
        ),
    )
    balance_transaction = models.CharField(
        max_length=255,
        help_text=_(
            'Balance transaction that describes the impact of this reversal '
            'on your account balance.',
        ),
    )
    charge = models.ForeignKey(
        'Charge',
        help_text=_(
            'ID of the charge that was ',
        ),
        on_delete=models.CASCADE,
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'It can be useful for storing additional information about the '
            'refund in a structured format.',
        ),
    )
    reason = models.CharField(
        max_length=255,
        choices=REFUND_CHOICES,
        help_text=_(
            'Reason for the refund. If set, possible values are duplicate, '
            'fraudulent, and requested_by_customer.',
        ),
    )
    receipt_number = models.CharField(
        max_length=255,
        help_text=_(
            'This is the transaction number that appears on email receipts '
            'sent for this refund.',
        ),
    )
    status = models.CharField(
        max_length=255,
        choices=REFUND_STATUS_CHOICES,
    )
    description = models.CharField(max_length=255)

    @classmethod
    def from_stripe_object(cls, stripe_object, charge=None):
        _dict = stripe_object.to_dict()
        _dict.pop('object')
        _dict.pop('charge')

        if charge:
            _dict['charge'] = charge
        else:
            Charge = cls._meta.get_field('charge').model
            Charge = cls.charge.field.related_model
            _dict['charge'] = Charge.from_stripe_object(
                stripe.Charge.retrieve(stripe_object.charge),
                descend=False,
            )

        s = cls(**_dict)
        s.save()
        return s
