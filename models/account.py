# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from ..utils import UnixDateTimeField
from .charge import CURRENCY_CHOICES

ACCOUNT_TYPES = (
    ('custom', _('Custom')),
    ('standard', _('Standard')),
)


class Account(models.Model):

    """Stripe Account object.

    This is an object representing your Stripe account. You can retrieve it to
    see properties on the account like its current e-mail address or if the
    account is enabled yet to make live charges.

    Some properties, marked as 'managed accounts only', are only available to
    platforms who want to create and manage Stripe accounts.
    """
    id = models.CharField(max_length=255, primary_key=True)
    charges_enabled = models.BooleanField(
        help_text=_(
            'Whether or not the account can create live charges',
        ),
    )
    country = models.CharField(  # todo: add CHOICES
        max_length=255,
        help_text=_('The country of the account')
    )
    currencies_supports = json.JSONField(
        help_text=_(
            'The currencies this account can submit when creating charges',
        ),
    )
    default_currency = models.CharField(
        max_length=255, help_text=_(
            'The currency this account has chosen to use as the default'),
        choices=CURRENCY_CHOICES)
    details_submitted = models.BooleanField(
        help_text=_(
            'Whether or not account details have been submitted yet. '
            'Standalone accounts cannot receive transfers before this is true.',
        ),
    )
    transfers_enabled = models.BooleanField(
        help_text=_(
            'Whether or not Stripe will send automatic transfers for this '
            'account. This is only false when Stripe is waiting for '
            'additional information from the account holder.',
        ),
        default=True,
    )
    display_name = models.CharField(
        max_length=255,
        help_text=_(
            'The display name for this account. This is used on the Stripe '
            'dashboard to help you differentiate between accounts.',
        ),
    )
    email = models.EmailField(help_text=_('The primary user’s email address'))
    statement_descriptor = models.TextField(
        help_text=_(
            'The text that will appear on credit card statements',
        ),
    )
    timezone = models.CharField(
        max_length=255,
        help_text=_(
            'The timezone used in the Stripe dashboard for this account. A '
            'list of possible timezone values is maintained at the IANA '
            'Timezone Database.',
        ),
    )
    business_name = models.CharField(
        max_length=255,
        help_text=_(
            'The publicly visible name of the business',
        ),
    )
    business_logo = models.CharField(max_length=255, null=True)
    business_url = models.URLField(
        help_text=_('The publicly visible website of the business'),
        null=True,
    )
    created = UnixDateTimeField()
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'charge in a structured format.',
        ),
    )
    support_email = models.EmailField(null=True)

    support_phone = models.CharField(
        max_length=255,
        help_text=_(
            'The publicly visible support phone number for the business',
        ),
        null=True,
    )
    payout_schedule = json.JSONField(null=True)
    payout_statement_descriptor = models.CharField(max_length=255, null=True)
    payouts_enabled = models.BooleanField()

    bank_accounts = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'Bank accounts currently attached to this account.',
        ),
    )
    debit_negative_balances = models.BooleanField(
        help_text=_(
            '(Managed Accounts Only) '
            'Whether or not Stripe will attempt to reclaim negative account '
            'balances from this account’s bank account.',
        ),
    )
    decline_charge_on = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'Account-level settings to automatically decline certain types of '
            'charges regardless of the bank’s decision.',
        ),
    )
    legal_entity = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'Information regarding the owner of this account, including '
            'verification status.',
        ),
    )
    product_description = models.TextField(
        help_text=_(
            '(Managed Accounts Only) '
            'An internal-only description of the product or service provided. '
            'This is used by Stripe in the event the account gets flagged for '
            'potential fraud.',
        ),
        null=True,
    )
    tos_acceptance = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'Who accepted the Stripe terms of service, and when they accepted '
            'it.',
        ),
    )
    transfer_schedule = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'When payments collected will be automatically paid out to the '
            'account holder’s bank account',
        ),
    )
    type = models.CharField(max_length=255, choices=ACCOUNT_TYPES)
    verification = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'That state of the account’s information requests, including what '
            'information is needed and by when it must be provided.',
        ),
    )

    @classmethod
    def from_stripe_object(cls, stripe_object):
        _dict = stripe_object.to_dict()
        _dict.pop('object')
        _dict.pop('external_accounts')  # todo: handle this
        a = cls(**_dict)
        a.save()

        return a
