# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from ..utils import UnixDateTimeField


class Customer(models.Model):

    """Stripe Customer object.

    Customer objects allow you to perform recurring charges and track multiple
    charges that are associated with the same customer. The API allows you to
    create, delete, and update your customers. You can retrieve individual
    customers as well as a list of all your customers.
    """

    id = models.CharField(max_length=255, primary_key=True)
    livemode = models.BooleanField()
    created = UnixDateTimeField()
    account_balance = models.IntegerField(
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
    default_source = models.ForeignKey(
        'PaymentMethod',
        help_text=_(
            'ID of the default payment method attached to this customer.',
        ),
        related_name='customers',
        on_delete=models.CASCADE,
        null=True,
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

    description = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
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

    sources = models.ManyToManyField(
        'Source',
        null=True,
    )

    @classmethod
    def from_stripe_object(cls, stripe_object, descend=True):
        """Turn Customer StripeObject from stripe-python into saved model.

        :param stripe_object:
        :type stripe_object: :class:`stripe.stripe_object.StripeObject`
        :param descend: Go deeper into subscriptions, default: True
        :type descend: bool
        :rtype: :class:`based.app.stripe.models.customer.Customer`
        :returns: saved model
        """
        _dict = stripe_object.to_dict()
        _dict.pop('object')

        if 'subscriptions' in _dict:
            _dict.pop('subscriptions')
        if 'sources' in _dict:
            _dict.pop('sources')
        if 'default_source' in _dict:
            _dict.pop('default_source')

        c = Customer(**_dict)
        c.save()

        if descend:
            Subscription = cls.subscription_set.rel.related_model
            for subscription in stripe_object.subscriptions.auto_paging_iter():
                c.subscription_set.add(
                    Subscription.from_stripe_object(subscription, customer=c),
                )

            Source = cls.sources.rel.related_model
            BankAccount = cls.bankaccount_set.rel.related_model
            Card = cls.card_set.rel.related_model
            for source in stripe_object.sources.auto_paging_iter():
                if source.object == 'bank_account':
                    c.bankaccount_set.add(
                        BankAccount.from_stripe_object(source, customer=c)
                    )
                elif source.object == 'card':
                    c.card_set.add(
                        Card.from_stripe_object(source, customer=c)
                    )
                else:
                    c.sources.add(
                        Source.from_stripe_object(source),
                    )
        return c
