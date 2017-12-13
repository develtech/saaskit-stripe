# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json


class Event(models.Model):

    """Stripe Event object.

    Events are our way of letting you know about something interesting that has
    just happened in your account. When an interesting event occurs, we create
    a new event object. For example, when a charge succeeds we create a
    ``charge.succeeded`` event; or, when an invoice can't be paid we create an
    ``invoice.payment_failed`` event. Note that many API requests may cause
    multiple events to be created. For example, if you create a new
    subscription for a customer, you will receive both a
    ``customer.subscription.created`` event and a ``charge.succeeded`` event.

    Like our other API resources, you can retrieve an individual event or a
    list of events from the API. We also have a system for sending the events
    directly to your server, called webhooks. Webhooks are managed in your
    account settings, and our webhook guide will help you get them set up.

    NOTE: Right now, we only guarantee access to events through the Retrieve
    Event API for 30 days.
    """

    livemode = models.BooleanField()
    created = models.DateTimeField()
    data = json.JSONField(
        help_text=_(
            'Hash containing data associated with the event.',
        ),
    )
    pending_webhooks = models.PositiveIntegerField(
        help_text=_(
            'Number of webhooks yet to be delivered successfully (return a '
            '20x response) to the URLs you’ve specified.',
        ),
    )
    type = models.CharField(
        max_length=255,
        help_text=_(
            'Description of the event: e.g. invoice.created, charge.refunded, '
            'etc.',
        ),
    )
    api_version = models.CharField(
        max_length=255,
        help_text=_(
            'The Stripe API version used to render data. Note: this property '
            'is populated for events on or after October 31, 2014.',
        ),
    )
    request = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the API request that caused the event. If null, the event '
            'was automatic (e.g. Stripe’s automatic subscription handling). '
            'Request logs are available in the dashboard but currently not in '
            'the API. Note: this property is populated for events on or after '
            'April 23, 2013.',
        ),
    )
