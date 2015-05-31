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


REFUND_CHOICES = (
    ("DUPLICATE", "duplicate"),
    ("FRAUDULENT", "fraudulent"),
    ("REQUESTED_BY_CUSTOMER", "requested_by_customer")
)

class Refund(models.Model):
    amount = models.IntegerField(
        help_text=_(
            "Amount reversed, in cents."
        )
    )
    created = models.DateTimeField()
    currency = models.IntegerField(
        help_text=_(
            "Three-letter ISO code representing the currency of the reversal."
        )
    )
    balance_transaction = models.CharField(
        max_length=255,
        help_text=_(
            "Balance transaction that describes the impact of this reversal on "
            "your account balance."
        )
    )
    charge = models.CharField(
        max_length=255,
        help_text=_(
            "ID of the charge that was "
        )
    )
    metadata = json.JSONField(
        help_text=_(
            "A set of key/value pairs that you can attach to a charge object. "
            "It can be useful for storing additional information about the "
            "charge in a structured format."
        )
    )
    reason = models.CharField(
        max_length=255,
        choices=REFUND_CHOICES,
        help_text=_(
            "Reason for the refund. If set, possible values are duplicate, "
            "fraudulent, and requested_by_customer."
        )
    )
    receipt_number = models.CharField(
        max_length=255,
        help_text=_(
            "This is the transaction number that appears on email receipts "
            "sent for this refund."
        )
    )
    description = models.CharField(max_length=255)

class Customer(models.Model):
    livemode = models.BooleanField()
    created = models.DateTimeField()
    account_balance = models.DateTimeField(
        help_text=_(
            "Current balance, if any, being stored on the customer’s account. "
            "If negative, the customer has credit to apply to the next "
            "invoice. If positive, the customer has an amount owed that will "
            "be added to the next invoice. The balance does not refer to any "
            "unpaid invoices; it solely takes into account amounts that have "
            "yet to be successfully applied to any invoice. This balance is "
            "only taken into account for recurring charges."
        )
    )
    currency = models.CharField(
        max_length=255,
        help_text=_(
            "The currency the customer can be charged in for recurring "
            "billing purposes (subscriptions, invoices, invoice items)."
        )
    )
    default_source = models.CharField(
        max_length=255,
        help_text=_(
            "ID of the default source attached to this customer."
        )
    )
    delinquent = models.CharField(
        max_length=255,
        help_text=_(
            "Whether or not the latest charge for the customer’s latest "
            "invoice has failed"
        )
    )
    discount = models.ForeignKey(
        "Discount",
        max_length=255,
        help_text=_(
            "Describes the current discount active on the customer, if there "
            "is one."
        )
    )
    description = models.CharField(max_length=255)
    email = models.EmailField()
    metadata = json.JSONField(
        help_text=_(
            "A set of key/value pairs that you can attach to a charge object. "
            "It can be useful for storing additional information about the "
            "charge in a structured format."
        )
    )

    sources = json.JSONField(
        help_text=_(
            "The customer’s payment sources, if any"
        )
    )
    subscriptions = models.ForeignKey(
        "Subscription",
        help_text=_(
            "The customer’s current subscriptions, if any"
        )
    )


BRAND_CHOICES = (
    ("VISA", "Visa"),
    ("AMERICAN_EXPRESS", "American Express"),
    ("MASTERCARD", "MasterCard"),
    ("DISCOVER", "Discover"),
    ("JCB", "JCB"),
    ("DINERS_CLUB", "Diners Club"),
    ("UNKNOWN", "Unknown"),
)

FUNDING_CHOICES = (
    ("CREDIT", "credit"),
    ("DEBIT", "debit"),
    ("PREPAID", "prepaid"),
    ("UNKNOWN", "unknown"),
)
CHECK_CHOICES=(
    ("PASS", "pass"),
    ("FAIL", "fail"),
    ("UNAVAILABLE", "unavailable"),
    ("UNCHECKED", "unchecked"),
)

class Card(models.Model):
    id = models.AutoField(
        primary_key=True,
        help_text=_(
            "ID of card (used in conjunction with a customer or recipient ID)"
        )
    )
    brand = models.CharField(
        choices=BRAND_CHOICES, max_length=255,
        help_text=_(
            "Card brand. Can be ``Visa``, ``American Express``, "
            "``MasterCard``, ``Discover``, ``JCB``, ``Diners Club``, "
            "or ``Unknown``."
        )
    )
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    funding = models.CharField(
        max_length=255,
        choices=FUNDING_CHOICES
    )
    last4 = models.PositiveIntegerField()
    address_city = models.CharField(max_length=255)
    address_country = models.CharField(
        max_length=255,
        help_text=_(
            "Billing address country, if provided when creating card"
        )
    )

    address_line1 = models.CharField(max_length=255)
    address_line1_check = models.CharField(
        max_length=255,
        help_text=_(
            "If ``address_line1`` was provided, results of the check: "
            "``pass``, ``fail``, ``unavailable``, or ``unchecked``."
        )
    )
    address_line2 = models.CharField(max_length=255)
    address_state = models.CharField(max_length=255)
    address_zip = models.CharField(max_length=255)
    address_zip_check = models.CharField(
        max_length=255,
        help_text=_(
            "If ``address_zip`` was provided, results of the check: "
            "``pass``, ``fail``, ``unavailable``, or ``unchecked``."
        )
    )

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
