# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json


class Customer(models.Model):

    """Stripe Customer object.

    Customer objects allow you to perform recurring charges and track multiple
    charges that are associated with the same customer. The API allows you to
    create, delete, and update your customers. You can retrieve individual
    customers as well as a list of all your customers.
    """

    livemode = models.BooleanField()
    created = models.DateTimeField()
    account_balance = models.DateTimeField(
        help_text=_(
            'Current balance, if any, being stored on the customer’s account. '
            'If negative, the customer has credit to apply to the next '
            'invoice. If positive, the customer has an amount owed that will '
            'be added to the next invoice. The balance does not refer to any '
            'unpaid invoices; it solely takes into account amounts that have '
            'yet to be successfully applied to any invoice. This balance is '
            'only taken into account for recurring charges.',
        ),
    )
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'The currency the customer can be charged in for recurring '
            'billing purposes (subscriptions, invoices, invoice items).',
        ),
    )
    default_source = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the default source attached to this customer.',
        ),
    )
    delinquent = models.CharField(
        max_length=255,
        help_text=_(
            'Whether or not the latest charge for the customer’s latest '
            'invoice has failed',
        ),
    )

    # Reverse
    # discount = models.ForeignKey(
    #     'Discount',
    #     max_length=255,
    #     help_text=_(
    #         'Describes the current discount active on the customer, if '
    #         'there is one.'
    #     )
    # )

    description = models.CharField(max_length=255)
    email = models.EmailField()
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'It can be useful for storing additional information about the '
            'customer in a structured format.',
        ),
    )

    sources = json.JSONField(
        help_text=_(
            'The customer’s payment sources, if any',
        ),
    )

    shipping = json.JSONField(
        help_text=_(
            'Mailing and shipping address for the customer. Appears on '
            'invoices emailed to this customer.',
        ),
    )

    # reverse relation
    # subscriptions = models.ForeignKey(
    #     'Subscription',
    #     help_text=_(
    #         'The customer’s current subscriptions, if any'
    #     )
    # )

    @staticmethod
    def from_stripe_object(stripe_object):

        for subscription in stripe_object.subscriptions.auto_paging_iter():
            print(subscription)

        _dict = stripe_object.to_dict()
        _dict.pop('object')
        _dict.pop('subscriptions')

        return Customer(**_dict)
