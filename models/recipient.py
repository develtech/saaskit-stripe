# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

RECIPIENT_TYPE_CHOICES = (
    ('individual', _('Individual')),
    ('corporoation', _('Corporation')),
)


class Recipient(models.Model):

    """Stripe Recipient object.

    With recipient objects, you can transfer money from your Stripe account to
    a third party bank account or debit card. The API allows you to create,
    delete, and update your recipients. You can retrieve individual recipients
    as well as a list of all your recipients.

    Recipient objects have been deprecated in favor of Connect, specifically
    the much more powerful account objects. Please use them instead. If you are
    already using recipients, please see our migration guide for more
    information.
    """

    livemode = models.BooleanField()
    created = models.DateTimeField()
    type = models.CharField(
        max_length=255, help_text=_(
            'Type of the recipient, one of ``individual`` or ``corporation``.',
        ), choices=RECIPIENT_TYPE_CHOICES)
    active_account = json.JSONField(
        help_text=_(
            'Hash describing the current account on the recipient, if there '
            'is one.',
        ),
    )
    description = models.TextField()
    email = models.EmailField()
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'recipient in a structured format.',
        ),
    )
    name = models.CharField(
        max_length=255,
        help_text=_(
            'Full, legal name of the recipient.',
        ),
    )
    cards = models.ManyToManyField('Card', related_name='recipients')
    default_card = models.ForeignKey(
        'Card',
        help_text=_(
            'The default card to use for creating transfers to this recipient.',
        ),
        related_name='recipients_default',
        on_delete=models.CASCADE,
    )
    migrated_to = models.CharField(max_length=255)
