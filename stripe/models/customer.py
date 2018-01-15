# -*- coding: utf-8 -*-
from django.apps import apps
from django.db import models
from django.utils.translation import ugettext_lazy as _

import stripe
from django_extensions.db.fields import json

from ..settings import get_saaskit_callback, get_saaskit_stripe_setting
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

    shipping = json.JSONField(
        help_text=_(
            'Mailing and shipping address for the customer. Appears on '
            'invoices emailed to this customer.',
        ),
    )

    customer_relation = models.OneToOneField(
        get_saaskit_stripe_setting('CUSTOMER_RELATION_TO'),
        on_delete=models.SET_NULL,
        null=get_saaskit_stripe_setting('CUSTOMER_RELATION_NULLABLE')
    )

    # reverse relation
    # subscriptions = models.ForeignKey(
    #     'Subscription',
    #     help_text=_(
    #         'The customer’s current subscriptions, if any'
    #     )
    # )

    # reverse
    # sources = models.ManyToManyField(
    #     'Source',
    #     null=True,
    # )

    @classmethod
    def from_stripe_object(cls, stripe_object, descend=True):
        """Turn Customer StripeObject from stripe-python into saved model.

        :param stripe_object:
        :type stripe_object: :class:`stripe.stripe_object.StripeObject`
        :param descend: Go deeper into subscriptions, default: True
        :type descend: bool
        :rtype: :class:`saaskit.app.stripe.models.customer.Customer`
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

        c = cls(**_dict)
        c.save()

        if descend:
            Subscription = cls.subscription_set.rel.related_model
            for subscription in stripe_object.subscriptions.auto_paging_iter():
                c.subscription_set.add(
                    Subscription.from_stripe_object(subscription, customer=c),
                )

            Source = cls.source_set.rel.related_model
            BankAccount = cls.bankaccount_set.rel.related_model
            Card = cls.card_set.rel.related_model
            for source in stripe_object.sources.auto_paging_iter():
                if source.object == 'bank_account':
                    pass
                    c.bankaccount_set.add(
                        BankAccount.from_stripe_object(source, customer=c))
                elif source.object == 'card':
                    c.card_set.add(Card.from_stripe_object(source, customer=c))
                elif source.object == 'bitcoin':
                    c.source_set.add(
                        Source.from_stripe_object(source, customer=c),
                    )
                elif source.object == 'account':  # TODO
                    pass
        return c


def on_remote_single_customer_found(customer_list):
    return next(customer_list.auto_paging_iter())


def on_remote_multiple_customers_found(customer_list):
    return next(customer_list.auto_paging_iter())


def find_or_create_stripe_customer(customer_rel_model):
    """Find / create stripe customer by ``CUSTOMER_RELATIONAL_MODEL`` instance.

    This exists to make customer lookups more resilient and have errors
    be more detectable.

    To assist developers in handling the most common exceptions, functions
    like this can be overridden via callbacks set in the settings. You can
    switch out anything from this whole function, to the specific exceptions
    detected in this default function.

    The CUSTOMER_RELATIONAL_MODEL allows a stripe customer to be associated
    with any model (e.g. User, the default).

    With this helper function, you can resolve instances such as:

    - related local customer not existing on stripe
    - whether or not to lookup an empty/wrong customer id via another field,
      such as email.
      - and, how to handle if multiple customers are found

    :param customer_relational_model: instance of django model being associated
        with stripe customer. This is configured via
        ``CUSTOMER_RELATIONAL_MODEL`` in ``SAASKIT_SETTINGS``.
    :type customer_relational_model: :class:`django:django.db.models.Model`
    :returns: stripe Customer object
    :rtype: :class:`stripe.stripe_object.StripeObject`
    """
    ModelClass = apps.get_model(
        get_saaskit_stripe_setting('CUSTOMER_RELATION_TO'),
    )
    assert isinstance(customer_rel_model, ModelClass)

    if hasattr(customer_rel_model, 'customer'):  # returning customer
        try:
            customer = stripe.Customer.retrieve(
                customer_rel_model.customer.id,
            )
        except stripe.error.InvalidRequestError as e:
            return get_saaskit_callback('on_remote_customer_not_found')(
                customer_rel_model,
                exception=e,
            )

    email = customer_rel_model.email
    customers = stripe.Customer.list(email=email)

    if len(customers) > 1:
        return get_saaskit_callback('on_remote_multiple_customers_found')(
            customer_list=customers,
        )
    elif len(customers) > 0:
        return get_saaskit_callback('on_remote_single_customer_found')(
            customer_list=customers,
        )

    customer = stripe.Customer.create(email=email)
    return customer
