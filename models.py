# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


from django_extensions.db.fields import json


STATUS_CHOICES = (
    ("SUCCEEDED", "succeeded"),
    ("FAILED", "failed"),
)

class Charge(models.Model):
    livemode = models.BooleanField(default=True)
    amount = models.IntegerField(
        help_text=_("Amount charged in cents")
    )
    captured = models.BooleanField(
        help_text=_(
            "If the charge was created without capturing, this boolean "
            "represents whether or not it is still uncaptured or has since "
            "been captured."
        )
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        help_text=_(
            "Three-letter ISO currency code representing the currency in which "
            "the charge was made."
        )
    )  # todo ISO 3char fields
    paid = models.BooleanField(
        help_text=_(
            "true if the charge succeeded, or was successfully authorized for "
            "later capture."
        )
    )
    refunded = models.BooleanField(
        help_text=_(
            "Whether or not the charge has been fully refunded. If the charge is "
            "only partially refunded, this attribute will still be false."
        )
    )
    # refunds = models.ManyToManyField("Refund")
    # A list of refunds that have been applied to the charge.
    source = json.JSONField(
        help_text=_(
            "For most Stripe users, the source of every charge is a credit or "
            "debit card. This hash is then the card object describing that "
            "card."
        )
    )
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES,
        help_text=_(
            "The status of the payment is either ``succeeded`` or ``failed``."
        )
    )
    amount_refunded = models.PositiveIntegerField(
        help_text=_(
            "Amount in cents refunded (can be less than the amount attribute "
            " on the charge if a partial refund was issued)."
        )
    )
    balance_transaction = models.CharField(
        max_length=255,
        help_text=_(
            "ID of the balance transaction that describes the impact of this "
            "charge on your account balance (not including refunds or "
            "disputes)."
        )
    )  # relation todo
    customer = models.ForeignKey(
        "Customer",
        help_text=_(
            "ID of the customer this charge is for if one exists."
        )
    )
    description = models.CharField(max_length=255)
    dispute = models.ForeignKey(
        "Dispute", blank=True, null=True,
        help_text=_(
            "Details about the dispute if the charge has been disputed."
        )
    )
    failure_code = models.CharField(
        max_length=255,
        help_text=_(
            "Error code explaining reason for charge failure if available (see "
            "the errors section for a list of codes)."
        )
    )
    failure_message = models.CharField(
        max_length=255,
        help_text=_(
            "Message to user further explaining reason for charge failure if "
            "available."
        )
    )
    invoice = models.ForeignKey(
        "Invoice",
        help_text=_(
            "ID of the invoice this charge is for if one exists."
        )
    )
    metadata = json.JSONField(
        help_text=_(
            "A set of key/value pairs that you can attach to a charge object. "
            "It can be useful for storing additional information about the "
            "charge in a structured format."
        )
    )
    receipt_email = models.EmailField(
        help_text=_(
            "This is the email address that the receipt for this charge was "
            "sent to."
        )
    )
    receipt_number = models.CharField(
        max_length=255,
        help_text=_(
            "This is the transaction number that appears on email receipts "
            "sent for this charge."
        )
    )
    application_fee = models.CharField(
        max_length=255,
        help_text=_(
            "The application fee (if any) for the charge. See the Connect "
            "documentation for details."
        )
    )
    destination = models.CharField(
        max_length=255,
        help_text=_(
            "The account (if any) the charge was made on behalf of. See the "
            "Connect documentation for details."
        )
    )
    fraud_details= json.JSONField(
        help_text=_(
            "Hash with information on fraud assessments for the charge. "
            "Assessments reported by you have the key ``user_report`` and, if "
            "set, possible values of ``safe`` and ``fraudulent``. Assessments "
            "from Stripe have the key ``stripe_report`` and, if set, the value "
            "fraudulent."
        )
    )
    shipping = json.JSONField(
        help_text=_(
            "Shipping information for the charge."
        )
    )
    transfer = models.CharField(
        help_text=_(
            "ID of the transfer to the ``destination`` account (only "
            "applicable if the charge was created using the ``destination`` "
            "parameter)."
        ),
        max_length=255
    )

class Refund(models.Model):
    amount = models.IntegerField()
    created = models.DateTimeField()
    currency = models.IntegerField()
    balance_transaction = models.CharField(max_length=255)
    charge = models.CharField(max_length=255)
    metadata = json.JSONField()
    reason = models.CharField(max_length=255)
    receipt_number = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

class Customer(models.Model):
    livemode = models.BooleanField()
    created = models.DateTimeField()
    account_balance = models.DateTimeField()
    currency = models.CharField(max_length=255)
    default_source = models.CharField(max_length=255)
    delinquent = models.CharField(max_length=255)
    discount = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    discount = models.ForeignKey('Discount')
    email = models.EmailField()
    metadata = json.JSONField()
    sources = json.JSONField()
    subscriptions = models.ForeignKey("Subscription")


BRAND_CHOICES = (
    ("VISA", "Visa"),
    ("AMERICAN_EXPRESS", "American Express"),
    ("MASTERCARD", "MasterCard"),
    ("DISCOVER", "Discover"),
    ("JCB", "JCB"),
    ("DINERS_CLUB", "Diners Club"),
    ("UNKNOWN", "Unknown"),
)

class Card(models.Model):
    brand = models.CharField(choices=BRAND_CHOICES, max_length=255)


class Subscription(models.Model):
    cancel_at_period_end =models.BooleanField()

class Plan(models.Model):
    pass

class Discount(models.Model):
    pass

class Invoice(models.Model):
    pass

class InvoiceItem(models.Model):
    pass

class Dispute(models.Model):
    pass

class Transfer(models.Model):
    pass

class TransferReversal(models.Model):
    pass

class Recipient(models.Model):
    pass

class ApplicationFee(models.Model):
    pass

class ApplicationFeeRefund(models.Model):
    pass

class Account(models.Model):
    pass

class Balance(models.Model):
    pass

class Event(models.Model):
    pass

class Token(models.Model):
    pass

class BitCoinReceiver(models.Model):
    pass
