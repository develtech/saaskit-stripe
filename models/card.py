# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

CARD_BRAND_CHOICES = (
    ('Visa', _('Visa')),
    ('American Express', _('American Express')),
    ('MasterCard', _('MasterCard')),
    ('Discover', _('Discover')),
    ('JCB', _('JCB')),
    ('Diners Club', _('Diners Club')),
    ('Unknown', _('Unknown')),
)

CARD_FUNDING_CHOICES = (
    ('credit', _('Credit')),
    ('debit', _('Debit')),
    ('prepaid', _('Prepaid')),
    ('unknown', _('Unknown')),
)
CARD_ADDRESS_CHECK_CHOICES = (
    ('pass', _('Pass')),
    ('fail', _('Fail')),
    ('unavailable', _('Unavailable')),
    ('unchecked', _('Unchecked')),
)

CARD_CVC_CHECK_CHOICES = (
    ('pass', _('Pass')),
    ('fail', _('Fail')),
    ('unavailable', _('Unavailable')),
    ('unchecked', _('Unchecked')),
)


class Card(models.Model):

    """Stripe Card object.

    You can store multiple cards on a customer in order to charge the customer
    later. You can also store multiple debit cards on a recipient in order to
    transfer to those cards later.
    """

    id = models.AutoField(
        primary_key=True,
        help_text=_(
            'ID of card (used in conjunction with a customer or recipient ID)'
        )
    )
    brand = models.CharField(
        choices=CARD_BRAND_CHOICES, max_length=255,
        help_text=_(
            'Card brand. Can be ``Visa``, ``American Express``, '
            '``MasterCard``, ``Discover``, ``JCB``, ``Diners Club``, '
            'or ``Unknown``.'
        )
    )
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    funding = models.CharField(
        max_length=255,
        choices=CARD_FUNDING_CHOICES
    )
    last4 = models.PositiveIntegerField()
    address_city = models.CharField(max_length=255)
    address_country = models.CharField(
        max_length=255,
        help_text=_(
            'Billing address country, if provided when creating card'
        )
    )

    address_line1 = models.CharField(max_length=255)
    address_line1_check = models.CharField(
        max_length=255,
        help_text=_(
            'If ``address_line1`` was provided, results of the check: '
            '``pass``, ``fail``, ``unavailable``, or ``unchecked``.'
        ),
        choices=CARD_ADDRESS_CHECK_CHOICES
    )
    address_line2 = models.CharField(max_length=255)
    address_state = models.CharField(max_length=255)
    address_zip = models.CharField(max_length=255)
    address_zip_check = models.CharField(
        max_length=255,
        help_text=_(
            'If ``address_zip`` was provided, results of the check: '
            '``pass``, ``fail``, ``unavailable``, or ``unchecked``.'
        ),
        choices=CARD_ADDRESS_CHECK_CHOICES
    )
    country = models.CharField(
        max_length=255,
        help_text=_(
            'Two-letter ISO code representing the country of the card. You '
            'could use this attribute to get a sense of the international '
            'breakdown of cards you’ve collected.'
        )
    )
    customer = models.ForeignKey(
        'Customer',
        help_text=_(
            'The customer that this card belongs to. This attribute will not '
            'be in the card object if the card belongs to a recipient instead.'
        ),
        on_delete=models.CASCADE
    )
    cvc_check = models.CharField(
        max_length=255,
        choices=CARD_CVC_CHECK_CHOICES
    )
    dynamic_last4 = models.CharField(
        max_length=4,
        help_text=_(
            '(For Apple Pay integrations only.) The last four digits of the '
            'device account number.'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'charge in a structured format.'
        )
    )
    name = models.CharField(
        max_length=255,
        help_text=_(
            'Cardholder name'
        )
    )
    # reverse from relation
    # recipient = models.CharField(
    #     max_length=255,
    #     help_text=_(
    #         'The recipient that this card belongs to. This attribute will '
    #         'not be in the card object if the card belongs to a customer '
    #         'instead.'
    #     )
    # )
    fingerprint = models.CharField(
        max_length=255,
        help_text=_(
            'Uniquely identifies this particular card number. You can use '
            'this attribute to check whether two customers who’ve signed up '
            'with you are using the same card number, for example.'
        )
    )
