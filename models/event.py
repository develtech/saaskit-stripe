# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json

from ..utils import UnixDateTimeField

EVENT_TYPES = (
    ('account.updated', _('Account Updated')),
    ('account.application.deauthorized', _('Account Application Deauthorized')),
    ('account.external_account.created', _('External Account Created')),
    ('account.external_account.deleted', _('External Account Deleted')),
    ('account.external_account.updated', _('External Account Updated')),
    ('application_fee.created', _('Application Fee Created')),
    ('application_fee.refunded', _('Application Fee Refunded')),
    ('application_fee.refund.updated', _('Application Refund Updated')),
    ('balance.available', _('Balance Updated')),
    ('charge.captured', _('Charge Captured')),
    ('charge.failed', _('Charge Failed')),
    ('charge.pending', _('Charge Pending')),
    ('charge.refunded', _('Charge Refunded')),
    ('charge.succeeded', _('Charge Succeeded')),
    ('charge.updated', _('Charge Updated')),
    ('charge.dispute.closed', _('Charge Dispute Closed')),
    ('charge.dispute.created', _('Charge Dispute Created')),
    ('charge.dispute.funds_reinstated', _('Charge Dispute - Funds Reinstated')),
    ('charge.dispute.funds_withdrawn', _('Charge Dispute - Funds Withdrawn')),
    ('charge.dispute.updated', _('Charge Dispute - Updated')),
    ('charge.refund.updated', _('Charge Refund - Updated')),
    ('coupon.created', _('Coupon Created')),
    ('coupon.deleted', _('Coupon Deleted')),
    ('coupon.updated', _('Coupon Updated')),
    ('customer.created', _('Customer Created')),
    ('customer.deleted', _('Customer Deleted')),
    ('customer.updated', _('Customer Updated')),
    ('customer.discount.created', _('Customer Discount Created')),
    ('customer.discount.deleted', _('Customer Discount Deleted')),
    ('customer.discount.updated', _('Customer Discount Updated')),
    ('customer.source.created', _('Customer Source Created')),
    ('customer.source.deleted', _('Customer Source Deleted')),
    ('customer.source.updated', _('Customer Source Updated')),
    ('customer.subscription.created', _('Customer Subscription Created')),
    ('customer.subscription.deleted', _('Customer Subscription Deleted')),
    (
        'customer.subscription.trial_will_end',
        _('Customer Subscription Trial Nearing Completion'),
    ),
    ('customer.subscription.updated', _('Customer Subscription Updated')),
    ('file.created', _('File Created')),
    ('invoice.created', _('Invoice Created')),
    ('invoice.payment_failed', _('Invoice Payment Failed')),
    ('invoice.payment_succeeded', _('Invoice Payment Succeeded')),
    ('invoice.sent', _('Invoice Sent')),
    ('invoice.upcoming', _('Invoice Upcoming')),
    ('invoice.updated', _('Invoice Updated')),
    ('invoiceitem.created', _('Invoice Item Created')),
    ('invoiceitem.deleted', _('Invoice Item Deleted')),
    ('invoiceitem.updated', _('Invoice Item Updated')),
    ('order.created', _('Order Created')),
    ('order.payment_failed', _('Order Payment Failed')),
    ('order.payment_succeeded', _('Order Payment Succeeded')),
    ('order.updated', _('Order Updated')),
    ('order_return.created', _('Order Created')),
    ('payout.canceled', _('Payout Canceled')),
    ('payout.created', _('Payout Created')),
    ('payout.failed', _('Payout Failed')),
    ('payout.paid', _('Payout Paid')),
    ('payout.updated', _('Payout Updated')),
    ('plan.created', _('Plan Created')),
    ('plan.deleted', _('Plan Deleted')),
    ('plan.updated', _('Plan Updated')),
    ('product.created', _('Product Created')),
    ('product.deleted', _('Product Deleted')),
    ('product.updated', _('Product Updated')),
    ('recipient.created', _('Recipient Created')),
    ('recipient.deleted', _('Recipient Deleted')),
    ('recipient.updated', _('Recipient Updated')),
    ('review.closed', _('Review Closed')),
    ('review.opened', _('Review Opened')),
    ('sigma.scheduled_query_run.created', _('Sigma query finished')),
    ('sku.created', _('SKU Created')),
    ('sku.deleted', _('SKU Deleted')),
    ('sku.updated', _('SKU Updated')),
    ('source.canceled', _('Source Canceled')),
    ('source.chargeable', _('Source Chargeable')),
    ('source.failed', _('Source Failed')),
    ('source.transaction.created', _('Source Transaction Created')),
    ('transfer.created', _('Transfer Created')),
    ('transfer.reversed', _('Transfer Reversed')),
    ('transfer.updated', _('Transfer Updated')),
    ('ping', _('Ping test')),
)


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
    id = models.CharField(max_length=255, primary_key=True)
    livemode = models.BooleanField()
    created = UnixDateTimeField()
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
        choices=EVENT_TYPES,
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

    @classmethod
    def from_stripe_object(cls, stripe_object):
        _dict = stripe_object.to_dict()
        _dict.pop('object')

        s = cls(**_dict)
        s.save()
        return s
