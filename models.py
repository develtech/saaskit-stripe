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
            "it can be useful for storing additional information about the "
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
    # reverse relation
    # subscriptions = models.ForeignKey(
    #     "Subscription",
    #     help_text=_(
    #         "The customer’s current subscriptions, if any"
    #     )
    # )


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

CVC_CHOICES = (
    ("PASS", "pass"),
    ("FAIL", "fail"),
    ("UNAVAILABLE", "unavailable"),
    ("UNCHECKED", "unchecked")
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
    country = models.CharField(
        max_length=255,
        help_text=_(
            "Two-letter ISO code representing the country of the card. You "
            "could use this attribute to get a sense of the international "
            "breakdown of cards you’ve collected."
        )
    )
    customer = models.ForeignKey(
        "Customer",
        help_text=_(
            "The customer that this card belongs to. This attribute will not "
            "be in the card object if the card belongs to a recipient instead."
        )
    )
    cvc_check = models.CharField(
        max_length=255,
        choices=CVC_CHOICES
    )
    dynamic_last4 = models.CharField(
        max_length=4,
        help_text=_(
            "(For Apple Pay integrations only.) The last four digits of the "
            "device account number."
        )
    )
    metadata = json.JSONField(
        help_text=_(
            "A set of key/value pairs that you can attach to a charge object. "
            "it can be useful for storing additional information about the "
            "charge in a structured format."
        )
    )
    name = models.CharField(
        max_length=255,
        help_text=_(
            "Cardholder name"
        )
    )
    recipient = models.CharField(
        max_length=255,
        help_text=_(
            "The recipient that this card belongs to. This attribute will not "
            "be in the card object if the card belongs to a customer instead."
        )
    )
    fingerprint = models.CharField(
        max_length=255,
        help_text=_(
            "Uniquely identifies this particular card number. You can use this "
            "attribute to check whether two customers who’ve signed up with "
            "you are using the same card number, for example."
        )
    )


SUBSCRIPTION_STATUS_CHOICES = (
    ("TRIALING", "trialing"),
    ("ACTIVE", "active"),
    ("PAST_DUE", "past_due"),
    ("CANCELED", "canceled"),
    ("UNPAID", "unpaid"),
)
class Subscription(models.Model):
    cancel_at_period_end = models.BooleanField(
        help_text=_(
            "If the subscription has been canceled with the ``at_period_end``"
            "flag set to ``true``, ``cancel_at_period_end`` on the "
            "subscription will be true. You can use this attribute to "
            "determine whether a subscription that has a status of active is "
            "scheduled to be canceled at the end of the current period."
        )
    )
    customer = models.ForeignKey("Customer")
    plan = models.ForeignKey(
        "Plan",
        help_text=_(
            "Hash describing the plan the customer is subscribed to"
        )
    )
    quantity = models.PositiveIntegerField()
    start = models.DateTimeField(
        help_text=_(
            "Date the subscription started"
        )
    )
    status = models.CharField(
        max_length=255,
        choices=SUBSCRIPTION_STATUS_CHOICES,
        help_text=_(
            "Possible values are ``trialing``, ``active``, ``past_due``, "
            "``canceled``, or ``unpaid``. A subscription still in its trial "
            "period is ``trialing`` and moves to ``active`` when the trial "
            "period is over. When payment to renew the subscription fails, "
            "the subscription becomes ``past_due``. After Stripe has "
            "exhausted all payment retry attempts, the subscription ends up "
            "with a status of either ``canceled`` or ``unpaid`` depending on "
            "your retry settings. Note that when a subscription has a status "
            "of ``unpaid``, no subsequent invoices will be attempted "
            "(invoices will be created, but then immediately automatically "
            "closed. Additionally, updating customer card details will not "
            "lead to Stripe retrying the latest invoice.). After receiving "
            "updated card details from a customer, you may choose to reopen "
            "and pay their closed invoices."
        )
    )
    application_fee_percent = models.CharField(
        max_length=255,
        help_text=_(
            "A positive decimal that represents the fee percentage of the "
            "subscription invoice amount that will be transferred to the "
            "application owner’s Stripe account each billing period."
        )
    )
    canceled_at = models.DateTimeField(
        help_text=_(
            "If the subscription has been canceled, the date of that "
            "cancellation. If the subscription was canceled with "
            "``cancel_at_period_end``, canceled_at will still reflect the "
            "date of the initial cancellation request, not the end of the "
            "subscription period when the subscription is automatically moved "
            "to a canceled state."
        )
    )
    current_period_start = models.DateTimeField(
        help_text=_(
            "End of the current period that the subscription has been "
            "invoiced for. At the end of this period, a new invoice will be "
            "created."
        )
    )
    discount = models.ForeignKey(
        "Discount",
        help_text=_(
            "Describes the current discount applied to this subscription, if "
            "there is one. When billing, a discount applied to a subscription "
            "overrides a discount applied on a customer-wide basis."
        )
    )
    ended_at = models.DateTimeField(
        help_text=_(
            "If the subscription has ended (either because it was canceled or "
            "because the customer was switched to a subscription to a new "
            "plan), the date the subscription ended"
        )
    )
    metadata = json.JSONField(
        help_text=_(
            "A set of key/value pairs that you can attach to a charge object. "
            "it can be useful for storing additional information about the "
            "charge in a structured format."
        )
    )
    trial_end = models.DateTimeField(
        help_text=_(
            "If the subscription has a trial, the end of that trial."
        )
    )
    trial_start = models.DateTimeField(
        help_text=_(
            "If the subscription has a trial, the beginning of that trial."
        )
    )
    tax_percent = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text=_(
            "If provided, each invoice created by this subscription will apply "
            "the tax rate, increasing the amount billed to the customer."
        )
    )


CURRENCY_CHOICES = (
    ("USD", "USD"),
)
PLAN_INTERVAL_CHOICES = (
    ("DAY", "day"),
    ("WEEK", "week"),
    ("MONTH", "month"),
    ("YEAR", "year"),
)
class Plan(models.Model):
    livemode = models.BooleanField()
    amount = models.PositiveIntegerField(
        help_text=_(
            "The amount in cents to be charged on the interval specified"
        )
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_("Currency in which the subscription will be charged")
    )
    interval = models.CharField(
        choices=PLAN_INTERVAL_CHOICES,
        max_length=255,
        help_text=_(
            "One of ``day``, ``week``, ``month`` or ``year``. The frequency "
            "with which a subscription should be billed."
        )
    )
    interval_count = models.PositiveIntegerField(
        help_text=_(
            "The number of intervals (specified in the ``interval`` property) "
            "between each subscription billing. For example, "
            "``interval=month`` and interval_count=3 bills every 3 months."
        )
    )
    name = models.CharField(
        max_length=255,
        help_text=_(
            "Display name of the plan"
        )
    )
    metadata = json.JSONField(
        help_text=_(
            "A set of key/value pairs that you can attach to a charge object. "
            "it can be useful for storing additional information about the "
            "charge in a structured format."
        )
    )
    trial_period_days = models.PositiveIntegerField(
        help_text=_(
            "Number of trial period days granted when subscribing a customer "
            "to this plan. Null if the plan has no trial period."
        )
    )
    statement_descriptor = models.CharField(
        max_length=255,
        help_text=(
            "Extra information about a charge for the customer’s credit card "
            "statement."
        )
    )

COUPON_DURATION_CHOICES = (
    ("FOREVER", "forever"),
    ("ONCE", "once"),
    ("REPREATING", "repeating"),
)
class Coupon(models.Model):
    livemode = models.BooleanField()
    created = models.DateTimeField()
    duration = models.CharField(
        max_length=255,
        choices=COUPON_DURATION_CHOICES,
        help_text=_(
            "One of ``forever``, ``once``, and ``repeating``. Describes how "
            "long a customer who applies this coupon will get the discount."
        )
    )
    amount_off = models.PositiveIntegerField(
        max_length=255,
        help_text=_(
            "Amount (in the ``currency`` specified) that will be taken off the "
            "subtotal of any invoices for this customer."
        )
    )
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_(
            "If ``amount_off`` has been set, the currency of the amount to "
            "take off."
        )
    )
    duration_in_months = models.PositiveIntegerField(
        help_text=_(
            "If ``duration`` is ``repeating``, the number of months the "
            "coupon applies. Null if coupon ``duration`` is ``forever``"
            "or ``once``."
        )
    )
    max_redemptions = models.PositiveIntegerField(
        help_text=_(
            "Maximum number of times this coupon can be redeemed, in total, "
            "before it is no longer valid."
        )
    )
    metadata = json.JSONField(
        help_text=_(
            "A set of key/value pairs that you can attach to a charge object. "
            "it can be useful for storing additional information about the "
            "charge in a structured format."
        )
    )
    percent_off = models.PositiveIntegerField(
        help_text=_(
            "Percent that will be taken off the subtotal of any invoices for "
            "this customer for the duration of the coupon. For example, a "
            "coupon with percent_off of 50 will make a $100 invoice $50 "
            "instead."
        )
    )
    redeem_by = models.DateTimeField(
        help_text=_(
            "Date after which the coupon can no longer be redeemed"
        )
    )
    times_redeemed = models.PositiveIntegerField(
        help_text=_(
            "Number of times this coupon has been applied to a customer."
        )
    )
    valid = models.BooleanField(
        help_text=_(
            "Taking account of the above properties, whether this coupon can "
            "still be applied to a customer"
        )
    )

class Discount(models.Model):
    coupon = models.ForeignKey(
        "Coupon",
        help_text=_(
            "Hash describing the coupon applied to create this discount"
        )
    )
    customer = models.ForeignKey("Customer")
    start = models.DateTimeField(
        help_text=_("Date that the coupon was applied")
    )
    end = models.DateTimeField(
        help_text=_(
            "If the coupon has a duration of ``once`` or ``repeating``, the "
            "date that this discount will end. If the coupon used has a "
            "forever duration, this attribute will be null."
        )
    )
    subscription = models.ForeignKey(
        "Subscription",
        help_text=_(
            "The subscription that this coupon is applied to, if it is applied "
            "to a particular subscription"
        )
    )


class Invoice(models.Model):
    livemode = models.BooleanField()
    amount_due = models.IntegerField(
        help_text=_(
            "Final amount due at this time for this invoice. If the invoice’s "
            "total is smaller than the minimum charge amount, for example, or "
            "if there is account credit that can be applied to the invoice, "
            "the ``amount_due`` may be 0. If there is a positive "
            "``starting_balance`` for the invoice (the customer owes money), "
            "the amount_due will also take that into account. The charge that "
            "gets generated for the invoice will be for the amount specified "
            "in amount_due."
        )
    )
    attempt_count = models.PositiveIntegerField(
        help_text=_(
            "Number of payment attempts made for this invoice, from the "
            "perspective of the payment retry schedule. Any payment attempt "
            "counts as the first attempt, and subsequently only automatic "
            "retries increment the attempt count. In other words, manual "
            "payment attempts after the first attempt do not affect the "
            "retry schedule."
        )
    )
    attempted = models.BooleanField(
        help_text=_(
            "Whether or not an attempt has been made to pay the invoice. An "
            "invoice is not attempted until 1 hour after the "
            "``invoice.created`` webhook, for example, so you might not want "
            "to display that invoice as unpaid to your users."
        )
    )
    closed = models.BooleanField(
        help_text=_(
            "Whether or not the invoice is still trying to collect payment. An "
            "invoice is closed if it’s either paid or it has been marked "
            "closed. A closed invoice will no longer attempt to collect "
            "payment."
        )
    )
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES
    )
    customer = models.ForeignKey("Customer")
    date = models.DateTimeField()
    forgiven = models.BooleanField(
        help_text=_(
            "Whether or not the invoice has been forgiven. Forgiving an "
            "invoice instructs us to update the subscription status as if the "
            "invoice were succcessfully paid. Once an invoice has been "
            "forgiven, it cannot be unforgiven or reopened"
        )
    )
    lines = json.JSONField(
        help_text=_(
            "The individual line items that make up the invoice. ``lines`` is "
            "sorted as follows: invoice items in reverse chronological order, "
            "followed by the subscription, if any."
        )
    )
    paid = models.BooleanField(
        help_text=_(
            "Whether or not payment was successfully collected for this "
            "invoice. An invoice can be paid (most commonly) with a charge or "
            "with credit from the customer’s account balance."
        )
    )
    period_end = models.DateTimeField(
        help_text=_(
            "End of the usage period during which invoice items were added to "
            "this invoice"
        )
    )
    period_start = models.DateTimeField(
        help_text=_(
            "Start of the usage period during which invoice items were added "
            "to this invoice"
        )
    )
    starting_balance = models.IntegerField(
        help_text=_(
            "Starting customer balance before attempting to pay invoice. If "
            "the invoice has not been attempted yet, this will be the current "
            "customer balance."
        )
    )
    subtotal = models.IntegerField(
        help_text=_(
            "Total of all subscriptions, invoice items, and prorations on the "
            "invoice before any discount is applied"
        )
    )
    total = models.IntegerField(
        help_text=_(
            "Total after discount"
        )
    )
    application_fee = models.IntegerField(
        help_text=_(
            "The fee in cents that will be applied to the invoice and "
            "transferred to the application owner’s Stripe account when the "
            "invoice is paid."
        )
    )
    charge = models.ForeignKey(
        "Charge",
        help_text=_(
            "ID of the latest charge generated for this invoice, if any."
        )
    )
    description = models.CharField(max_length=255)
    discount = models.ForeignKey("Discount")
    ending_balance = models.IntegerField(
        help_text=_(
            "Ending customer balance after attempting to pay invoice. If the "
            "invoice has not been attempted yet, this will be null."
        )
    )
    next_payment_attempt = models.DateTimeField(
        help_text=_(
            "The time at which payment will next be attempted."
        )
    )
    receipt_number = models.CharField(
        max_length=255,
        help_text=_(
            "This is the transaction number that appears on email receipts "
            "sent for this invoice."
        )
    )
    statement_descriptor = models.CharField(
        max_length=255,
        help_text=_(
            "Extra information about an invoice for the customer’s credit card "
            "statement."
        )
    )
    subscription = models.ForeignKey(
        "Subscription",
        help_text=_(
            "The subscription that this invoice was prepared for, if any."
        )
    )
    webhooks_delivered_at = models.DateTimeField(
        help_text=_(
            "The time at which webhooks for this invoice were successfully "
            "delivered (if the invoice had no webhooks to deliver, this will "
            "match ``date``). Invoice payment is delayed until webhooks are "
            "delivered, or until all webhook delivery attempts have been "
            "exhausted."
        )
    )
    metadata = json.JSONField(
        help_text=_(
            "A set of key/value pairs that you can attach to a charge object. "
            "it can be useful for storing additional information about the "
            "charge in a structured format."
        )
    )
    subscription_proration_date = models.IntegerField(
        help_text=_(
            "Only set for upcoming invoices that preview prorations. The time "
            "used to calculate prorations."
        )
    )
    tax = models.IntegerField(
        help_text=_(
            "The amount of tax included in the total, calculated from "
            "``tax_percent`` and the subtotal. If no ``tax_percent`` is "
            "defined, this value will be null."
        )
    )
    tax_percent = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text=_(
            "This percentage of the subtotal has been added to the total "
            "amount of the invoice, including invoice line items and "
            "discounts. This field is inherited from the subscription’s "
            "``tax_percent`` field, but can be changed before the invoice is "
            "paid. This field defaults to null."
        )
    )


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
