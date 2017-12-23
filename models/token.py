# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..utils import UnixDateTimeField

TOKEN_TYPE_CHOICES = (
    ('card', _('Card')),
    ('bank_account', _('Bank Account')),
)


class Token(models.Model):

    """Stripe Token object.

    Often you want to be able to charge credit cards or send payments to bank
    accounts without having to hold sensitive card information on your own
    servers. Stripe.js makes this easy in the browser, but you can use the same
    technique in other environments with our token API.

    Tokens can be created with your publishable API key, which can safely be
    embedded in downloadable applications like iPhone and Android apps. You can
    then use a token anywhere in our API that a card or bank account is
    accepted. Note that tokens are not meant to be stored or used more than
    once—to store these details for use later, you should create Customer or
    Recipient objects.
    """
    id = models.CharField(max_length=255, primary_key=True)
    livemode = models.BooleanField()
    created = UnixDateTimeField()
    type = models.CharField(
        max_length=255,
        choices=TOKEN_TYPE_CHOICES,
        help_text=_(
            'Type of the token: ``card`` or ``bank_account``',
        ),
    )
    used = models.BooleanField(
        help_text=_(
            'Whether or not this token has already been used (tokens can be '
            'used only once)',
        ),
    )
    bank_account = models.ForeignKey(
        'BankAccount',
        help_text=_(
            'Hash describing the bank account',
        ),
        on_delete=models.CASCADE,
        null=True,
    )
    card = models.ForeignKey(
        'Card',
        help_text=_(
            'Hash describing the bank account',
        ),
        on_delete=models.CASCADE,
        null=True,
    )
    client_ip = models.CharField(
        max_length=255,
        help_text=_(
            'IP address of the client that generated the token',
        ),
    )

    @classmethod
    def from_stripe_object(cls, stripe_object):
        _dict = stripe_object.to_dict()
        _dict.pop('object')

        if 'card' in _dict:
            Card = cls.card.field.related_model
            _dict['card'] = Card.from_stripe_object(
                stripe_object.card,
                customer=None,
            )
        elif 'bank_account' in _dict:
            BankAccount = cls.bank_account.field.related_model
            _dict['bank_account'] = BankAccount.from_stripe_object(
                stripe_object.bank_account,
            )

        s = cls(**_dict)
        s.save()
        return s
