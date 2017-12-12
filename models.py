# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


from django_extensions.db.fields import json

CURRENCY_CHOICES = (
    ('USD', 'USD'),

    ('AED', 'United Arab Emirates Dirham'),
    ('AFN', 'Afghan Afghani'),
    ('ALL', 'Albanian Lek'),
    ('AMD', 'Armenian Dram'),
    ('ANG', 'Netherlands Antillean Gulden'),
    ('AOA', 'Angolan Kwanza'),
    ('ARS', 'Argentine Peso'),
    ('AUD', 'Australian Dollar'),
    ('AWG', 'Aruban Florin'),
    ('AZN', 'Azerbaijani Manat'),
    ('BAM', 'Bosnia & Herzegovina Convertible Mark'),
    ('BBD', 'Barbadian Dollar'),
    ('BDT', 'Bangladeshi Taka'),
    ('BGN', 'Bulgarian Lev'),
    ('BIF', 'Burundian Franc'),
    ('BMD', 'Bermudian Dollar'),
    ('BND', 'Brunei Dollar'),
    ('BOB', 'Bolivian Boliviano*'),
    ('BRL', 'Brazilian Real*'),
    ('BSD', 'Bahamian Dollar'),
    ('BWP', 'Botswana Pula'),
    ('BZD', 'Belize Dollar'),
    ('CAD', 'Canadian Dollar'),
    ('CDF', 'Congolese Franc'),
    ('CHF', 'Swiss Franc'),
    ('CLP', 'Chilean Peso*'),
    ('CNY', 'Chinese Renminbi Yuan'),
    ('COP', 'Colombian Peso*'),
    ('CRC', 'Costa Rican Colón*'),
    ('CVE', 'Cape Verdean Escudo*'),
    ('CZK', 'Czech Koruna*'),
    ('DJF', 'Djiboutian Franc*'),
    ('DKK', 'Danish Krone'),
    ('DOP', 'Dominican Peso'),
    ('DZD', 'Algerian Dinar'),
    ('EEK', 'Estonian Kroon*'),
    ('EGP', 'Egyptian Pound'),
    ('ETB', 'Ethiopian Birr'),
    ('EUR', 'Euro'),
    ('FJD', 'Fijian Dollar'),
    ('FKP', 'Falkland Islands Pound*'),
    ('GBP', 'British Pound'),
    ('GEL', 'Georgian Lari'),
    ('GIP', 'Gibraltar Pound'),
    ('GMD', 'Gambian Dalasi'),
    ('GNF', 'Guinean Franc*'),
    ('GTQ', 'Guatemalan Quetzal*'),
    ('GYD', 'Guyanese Dollar'),
    ('HKD', 'Hong Kong Dollar'),
    ('HNL', 'Honduran Lempira*'),
    ('HRK', 'Croatian Kuna'),
    ('HTG', 'Haitian Gourde'),
    ('HUF', 'Hungarian Forint*'),
    ('IDR', 'Indonesian Rupiah'),
    ('ILS', 'Israeli New Sheqel'),
    ('INR', 'Indian Rupee*'),
    ('ISK', 'Icelandic Króna'),
    ('JMD', 'Jamaican Dollar'),
    ('JPY', 'Japanese Yen'),
    ('KES', 'Kenyan Shilling'),
    ('KGS', 'Kyrgyzstani Som'),
    ('KHR', 'Cambodian Riel'),
    ('KMF', 'Comorian Franc'),
    ('KRW', 'South Korean Won'),
    ('KYD', 'Cayman Islands Dollar'),
    ('KZT', 'Kazakhstani Tenge'),
    ('LAK', 'Lao Kip*'),
    ('LBP', 'Lebanese Pound'),
    ('LKR', 'Sri Lankan Rupee'),
    ('LRD', 'Liberian Dollar'),
    ('LSL', 'Lesotho Loti'),
    ('LTL', 'Lithuanian Litas'),
    ('LVL', 'Latvian Lats'),
    ('MAD', 'Moroccan Dirham'),
    ('MDL', 'Moldovan Leu'),
    ('MGA', 'Malagasy Ariary'),
    ('MKD', 'Macedonian Denar'),
    ('MNT', 'Mongolian Tögrög'),
    ('MOP', 'Macanese Pataca'),
    ('MRO', 'Mauritanian Ouguiya'),
    ('MUR', 'Mauritian Rupee*'),
    ('MVR', 'Maldivian Rufiyaa'),
    ('MWK', 'Malawian Kwacha'),
    ('MXN', 'Mexican Peso*'),
    ('MYR', 'Malaysian Ringgit'),
    ('MZN', 'Mozambican Metical'),
    ('NAD', 'Namibian Dollar'),
    ('NGN', 'Nigerian Naira'),
    ('NIO', 'Nicaraguan Córdoba*'),
    ('NOK', 'Norwegian Krone'),
    ('NPR', 'Nepalese Rupee'),
    ('NZD', 'New Zealand Dollar'),
    ('PAB', 'Panamanian Balboa*'),
    ('PEN', 'Peruvian Nuevo Sol*'),
    ('PGK', 'Papua New Guinean Kina'),
    ('PHP', 'Philippine Peso'),
    ('PKR', 'Pakistani Rupee'),
    ('PLN', 'Polish Złoty'),
    ('PYG', 'Paraguayan Guaraní*'),
    ('QAR', 'Qatari Riyal'),
    ('RON', 'Romanian Leu'),
    ('RSD', 'Serbian Dinar'),
    ('RUB', 'Russian Ruble'),
    ('RWF', 'Rwandan Franc'),
    ('SAR', 'Saudi Riyal'),
    ('SBD', 'Solomon Islands Dollar'),
    ('SCR', 'Seychellois Rupee'),
    ('SEK', 'Swedish Krona'),
    ('SGD', 'Singapore Dollar'),
    ('SHP', 'Saint Helenian Pound*'),
    ('SLL', 'Sierra Leonean Leone'),
    ('SOS', 'Somali Shilling'),
    ('SRD', 'Surinamese Dollar*'),
    ('STD', 'São Tomé and Príncipe Dobra'),
    ('SVC', 'Salvadoran Colón*'),
    ('SZL', 'Swazi Lilangeni'),
    ('THB', 'Thai Baht'),
    ('TJS', 'Tajikistani Somoni'),
    ('TOP', 'Tongan Paʻanga'),
    ('TRY', 'Turkish Lira'),
    ('TTD', 'Trinidad and Tobago Dollar'),
    ('TWD', 'New Taiwan Dollar'),
    ('TZS', 'Tanzanian Shilling'),
    ('UAH', 'Ukrainian Hryvnia'),
    ('UGX', 'Ugandan Shilling'),
    ('USD', 'United States Dollar'),
    ('UYU', 'Uruguayan Peso*'),
    ('UZS', 'Uzbekistani Som'),
    ('VND', 'Vietnamese Đồng'),
    ('VUV', 'Vanuatu Vatu'),
    ('WST', 'Samoan Tala'),
    ('XAF', 'Central African Cfa Franc'),
    ('XCD', 'East Caribbean Dollar'),
    ('XOF', 'West African Cfa Franc*'),
    ('XPF', 'Cfp Franc*'),
    ('YER', 'Yemeni Rial'),
    ('ZAR', 'South African Rand'),
    ('ZMW', 'Zambian Kwacha'),
    )


CHARGE_STATUS_CHOICES = (
    ('succeeded', _('Charge succeeded')),
    ('failed', _('Charge failed')),
)

CHARGE_FAILURE_CHOICES = (
    (
        'incorrect_number',
        _('The card number is incorrect')
    ),
)


class Charge(models.Model):

    """Stripe Charge Object.

    To charge a credit or a debit card, you create a charge object. You can
    retrieve and refund individual charges as well as list all charges. Charges
    are identified by a unique random ID.
    """

    livemode = models.BooleanField(default=True)
    amount = models.IntegerField(
        help_text=_('Amount charged in cents'),
    )
    captured = models.BooleanField(
        help_text=_(
            'If the charge was created without capturing, this boolean '
            'represents whether or not it is still uncaptured or has since '
            'been captured.',
        ),
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'Three-letter ISO currency code representing the currency in '
            'which the charge was made.',
        ),
        choices=CURRENCY_CHOICES,
    )
    paid = models.BooleanField(
        help_text=_(
            'true if the charge succeeded, or was successfully authorized for '
            'later capture.',
        ),
    )
    refunded = models.BooleanField(
        help_text=_(
            'Whether or not the charge has been fully refunded. If the charge '
            'is only partially refunded, this attribute will still be false.'
        ),
    )
    # refunds = models.ManyToManyField('Refund')
    # A list of refunds that have been applied to the charge.
    source = json.JSONField(
        help_text=_(
            'For most Stripe users, the source of every charge is a credit or '
            'debit card. This hash is then the card object describing that '
            'card.',
        ),
    )
    status = models.CharField(
        max_length=255,
        choices=CHARGE_STATUS_CHOICES,
        help_text=_(
            'The status of the payment is either ``succeeded`` or ``failed``.',
        ),
    )
    amount_refunded = models.PositiveIntegerField(
        help_text=_(
            'Amount in cents refunded (can be less than the amount attribute '
            ' on the charge if a partial refund was issued).'
        )
    )
    balance_transaction = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the balance transaction that describes the impact of this '
            'charge on your account balance (not including refunds or '
            'disputes).',
        ),
    )  # relation todo
    customer = models.ForeignKey(
        'Customer',
        help_text=_(
            'ID of the customer this charge is for if one exists.',
        ),
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255)
    dispute = models.ForeignKey(
        'Dispute', blank=True, null=True,
        help_text=_(
            'Details about the dispute if the charge has been disputed.',
        ),
        on_delete=models.CASCADE
    )
    failure_code = models.CharField(
        max_length=255,
        help_text=_(
            'Error code explaining reason for charge failure if available '
            '(see the errors section for a list of codes).',
        ),
        choices=CHARGE_FAILURE_CHOICES,
    )
    failure_message = models.CharField(
        max_length=255,
        help_text=_(
            'Message to user further explaining reason for charge failure if '
            'available.',
        ),
    )
    invoice = models.ForeignKey(
        'Invoice',
        help_text=_(
            'ID of the invoice this charge is for if one exists.',
        ),
        on_delete=models.CASCADE
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'charge in a structured format.',
        ),
    )
    receipt_email = models.EmailField(
        help_text=_(
            'This is the email address that the receipt for this charge was '
            'sent to.',
        ),
    )
    receipt_number = models.CharField(
        max_length=255,
        help_text=_(
            'This is the transaction number that appears on email receipts '
            'sent for this charge.',
        ),
    )
    application_fee = models.CharField(
        max_length=255,
        help_text=_(
            'The application fee (if any) for the charge. See the Connect '
            'documentation for details.',
        ),
    )
    destination = models.CharField(
        max_length=255,
        help_text=_(
            'The account (if any) the charge was made on behalf of. See the '
            'Connect documentation for details.',
        ),
    )
    fraud_details = json.JSONField(
        help_text=_(
            'Hash with information on fraud assessments for the charge. '
            'Assessments reported by you have the key ``user_report`` and, if '
            'set, possible values of ``safe`` and ``fraudulent``. Assessments '
            'from Stripe have the key ``stripe_report`` and, if set, the '
            'value fraudulent.',
        ),
    )
    shipping = json.JSONField(
        help_text=_(
            'Shipping information for the charge.',
        ),
    )
    transfer = models.CharField(
        help_text=_(
            'ID of the transfer to the ``destination`` account (only '
            'applicable if the charge was created using the ``destination`` '
            'parameter).',
        ),
        max_length=255,
    )


REFUND_CHOICES = (
    ('duplicate', _('Duplicate')),
    ('fraudulent', _('Fraudulent')),
    ('requested_by_customer', _('Requested by customer')),
)


class Refund(models.Model):

    """Stripe Refund objects.

    Refund objects allow you to refund a charge that has previously been
    created but not yet refunded. Funds will be refunded to the credit or debit
    card that was originally charged. The fees you were originally charged are
    also refunded.
    """

    amount = models.IntegerField(
        help_text=_(
            'Amount reversed, in cents.'
        )
    )
    created = models.DateTimeField()
    currency = models.IntegerField(
        help_text=_(
            'Three-letter ISO code representing the currency of the reversal.'
        )
    )
    balance_transaction = models.CharField(
        max_length=255,
        help_text=_(
            'Balance transaction that describes the impact of this reversal '
            'on your account balance.'
        )
    )
    charge = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the charge that was '
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'It can be useful for storing additional information about the '
            'refund in a structured format.'
        )
    )
    reason = models.CharField(
        max_length=255,
        choices=REFUND_CHOICES,
        help_text=_(
            'Reason for the refund. If set, possible values are duplicate, '
            'fraudulent, and requested_by_customer.'
        )
    )
    receipt_number = models.CharField(
        max_length=255,
        help_text=_(
            'This is the transaction number that appears on email receipts '
            'sent for this refund.'
        )
    )
    description = models.CharField(max_length=255)


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
            'only taken into account for recurring charges.'
        )
    )
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'The currency the customer can be charged in for recurring '
            'billing purposes (subscriptions, invoices, invoice items).'
        )
    )
    default_source = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the default source attached to this customer.'
        )
    )
    delinquent = models.CharField(
        max_length=255,
        help_text=_(
            'Whether or not the latest charge for the customer’s latest '
            'invoice has failed'
        )
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
            'customer in a structured format.'
        )
    )

    sources = json.JSONField(
        help_text=_(
            'The customer’s payment sources, if any'
        )
    )
    # reverse relation
    # subscriptions = models.ForeignKey(
    #     'Subscription',
    #     help_text=_(
    #         'The customer’s current subscriptions, if any'
    #     )
    # )


CARD_BRAND_CHOICES = (
    ('Visa', _('Visa')),
    ('American Express', _('American Express')),
    ('MasterCard', _('MasterCard')),
    ('Discover', _('Discover')),
    ('JCB', _('JCB')),
    ('Diners Club', _('Diners Club')),
    ('Unknown', _('Unknown')),
)

CARD_FUNDING_CHOICES = (
    ('credit', _('Credit')),
    ('debit', _('Debit')),
    ('prepaid', _('Prepaid')),
    ('unknown', _('Unknown')),
)
CARD_ADDRESS_CHECK_CHOICES = (
    ('pass', _('Pass')),
    ('fail', _('Fail')),
    ('unavailable', _('Unavailable')),
    ('unchecked', _('Unchecked')),
)

CARD_CVC_CHECK_CHOICES = (
    ('pass', _('Pass')),
    ('fail', _('Fail')),
    ('unavailable', _('Unavailable')),
    ('unchecked', _('Unchecked')),
)


class Card(models.Model):

    """Stripe Card object.

    You can store multiple cards on a customer in order to charge the customer
    later. You can also store multiple debit cards on a recipient in order to
    transfer to those cards later.
    """

    id = models.AutoField(
        primary_key=True,
        help_text=_(
            'ID of card (used in conjunction with a customer or recipient ID)'
        )
    )
    brand = models.CharField(
        choices=CARD_BRAND_CHOICES, max_length=255,
        help_text=_(
            'Card brand. Can be ``Visa``, ``American Express``, '
            '``MasterCard``, ``Discover``, ``JCB``, ``Diners Club``, '
            'or ``Unknown``.'
        )
    )
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    funding = models.CharField(
        max_length=255,
        choices=CARD_FUNDING_CHOICES
    )
    last4 = models.PositiveIntegerField()
    address_city = models.CharField(max_length=255)
    address_country = models.CharField(
        max_length=255,
        help_text=_(
            'Billing address country, if provided when creating card'
        )
    )

    address_line1 = models.CharField(max_length=255)
    address_line1_check = models.CharField(
        max_length=255,
        help_text=_(
            'If ``address_line1`` was provided, results of the check: '
            '``pass``, ``fail``, ``unavailable``, or ``unchecked``.'
        ),
        choices=CARD_ADDRESS_CHECK_CHOICES
    )
    address_line2 = models.CharField(max_length=255)
    address_state = models.CharField(max_length=255)
    address_zip = models.CharField(max_length=255)
    address_zip_check = models.CharField(
        max_length=255,
        help_text=_(
            'If ``address_zip`` was provided, results of the check: '
            '``pass``, ``fail``, ``unavailable``, or ``unchecked``.'
        ),
        choices=CARD_ADDRESS_CHECK_CHOICES
    )
    country = models.CharField(
        max_length=255,
        help_text=_(
            'Two-letter ISO code representing the country of the card. You '
            'could use this attribute to get a sense of the international '
            'breakdown of cards you’ve collected.'
        )
    )
    customer = models.ForeignKey(
        'Customer',
        help_text=_(
            'The customer that this card belongs to. This attribute will not '
            'be in the card object if the card belongs to a recipient instead.'
        ),
        on_delete=models.CASCADE
    )
    cvc_check = models.CharField(
        max_length=255,
        choices=CARD_CVC_CHECK_CHOICES
    )
    dynamic_last4 = models.CharField(
        max_length=4,
        help_text=_(
            '(For Apple Pay integrations only.) The last four digits of the '
            'device account number.'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'charge in a structured format.'
        )
    )
    name = models.CharField(
        max_length=255,
        help_text=_(
            'Cardholder name'
        )
    )
    # reverse from relation
    # recipient = models.CharField(
    #     max_length=255,
    #     help_text=_(
    #         'The recipient that this card belongs to. This attribute will '
    #         'not be in the card object if the card belongs to a customer '
    #         'instead.'
    #     )
    # )
    fingerprint = models.CharField(
        max_length=255,
        help_text=_(
            'Uniquely identifies this particular card number. You can use '
            'this attribute to check whether two customers who’ve signed up '
            'with you are using the same card number, for example.'
        )
    )


SUBSCRIPTION_STATUS_CHOICES = (
    ('trialing', _('Trialing')),
    ('active', _('Active')),
    ('past_due', _('Past due')),
    ('canceled', _('Canceled')),
    ('unpaid', _('Unpaid')),
)


class Subscription(models.Model):

    """Stripe subscription object.

    Subscriptions allow you to charge a customer's card on a recurring basis. A
    subscription ties a customer to a particular plan `you've created`_.

    .. _you've created: https://stripe.com/docs/api#create_plan
    """

    cancel_at_period_end = models.BooleanField(
        help_text=_(
            'If the subscription has been canceled with the ``at_period_end``'
            'flag set to ``true``, ``cancel_at_period_end`` on the '
            'subscription will be true. You can use this attribute to '
            'determine whether a subscription that has a status of active is '
            'scheduled to be canceled at the end of the current period.',
        ),
    )
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,)
    plan = models.ForeignKey(
        'Plan',
        help_text=_(
            'Hash describing the plan the customer is subscribed to',
        ),
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField()
    start = models.DateTimeField(
        help_text=_(
            'Date the subscription started',
        ),
    )
    status = models.CharField(
        max_length=255,
        choices=SUBSCRIPTION_STATUS_CHOICES,
        help_text=_(
            'Possible values are ``trialing``, ``active``, ``past_due``, '
            '``canceled``, or ``unpaid``. A subscription still in its trial '
            'period is ``trialing`` and moves to ``active`` when the trial '
            'period is over. When payment to renew the subscription fails, '
            'the subscription becomes ``past_due``. After Stripe has '
            'exhausted all payment retry attempts, the subscription ends up '
            'with a status of either ``canceled`` or ``unpaid`` depending on '
            'your retry settings. Note that when a subscription has a status '
            'of ``unpaid``, no subsequent invoices will be attempted '
            '(invoices will be created, but then immediately automatically '
            'closed. Additionally, updating customer card details will not '
            'lead to Stripe retrying the latest invoice.). After receiving '
            'updated card details from a customer, you may choose to reopen '
            'and pay their closed invoices.'
        )
    )
    application_fee_percent = models.CharField(
        max_length=255,
        help_text=_(
            'A positive decimal that represents the fee percentage of the '
            'subscription invoice amount that will be transferred to the '
            'application owner’s Stripe account each billing period.'
        )
    )
    canceled_at = models.DateTimeField(
        help_text=_(
            'If the subscription has been canceled, the date of that '
            'cancellation. If the subscription was canceled with '
            '``cancel_at_period_end``, canceled_at will still reflect the '
            'date of the initial cancellation request, not the end of the '
            'subscription period when the subscription is automatically moved '
            'to a canceled state.'
        )
    )
    current_period_start = models.DateTimeField(
        help_text=_(
            'End of the current period that the subscription has been '
            'invoiced for. At the end of this period, a new invoice will be '
            'created.'
        )
    )
    discount = models.ForeignKey(
        'Discount',
        help_text=_(
            'Describes the current discount applied to this subscription, if '
            'there is one. When billing, a discount applied to a subscription '
            'overrides a discount applied on a customer-wide basis.',
        ),
        on_delete=models.CASCADE
    )
    ended_at = models.DateTimeField(
        help_text=_(
            'If the subscription has ended (either because it was canceled or '
            'because the customer was switched to a subscription to a new '
            'plan), the date the subscription ended'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'subscription in a structured format.'
        )
    )
    trial_end = models.DateTimeField(
        help_text=_(
            'If the subscription has a trial, the end of that trial.'
        )
    )
    trial_start = models.DateTimeField(
        help_text=_(
            'If the subscription has a trial, the beginning of that trial.'
        )
    )
    tax_percent = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text=_(
            'If provided, each invoice created by this subscription will '
            'apply the tax rate, increasing the amount billed to the customer.'
        )
    )


PLAN_INTERVAL_CHOICES = (
    ('day', _('Day')),
    ('week', _('Week')),
    ('month', _('Month')),
    ('year', _('Year')),
)


class Plan(models.Model):

    """Stripe Plan object.

    A subscription plan contains the pricing information for different products
    and feature levels on your site. For example, you might have a $10/month
    plan for basic features and a different $20/month plan for premium
    features.
    """

    livemode = models.BooleanField()
    amount = models.PositiveIntegerField(
        help_text=_(
            'The amount in cents to be charged on the interval specified'
        )
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_('Currency in which the subscription will be charged')
    )
    interval = models.CharField(
        choices=PLAN_INTERVAL_CHOICES,
        max_length=255,
        help_text=_(
            'One of ``day``, ``week``, ``month`` or ``year``. The frequency '
            'with which a subscription should be billed.'
        )
    )
    interval_count = models.PositiveIntegerField(
        help_text=_(
            'The number of intervals (specified in the ``interval`` property) '
            'between each subscription billing. For example, '
            '``interval=month`` and interval_count=3 bills every 3 months.'
        )
    )
    name = models.CharField(
        max_length=255,
        help_text=_(
            'Display name of the plan'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'plan in a structured format.'
        )
    )
    trial_period_days = models.PositiveIntegerField(
        help_text=_(
            'Number of trial period days granted when subscribing a customer '
            'to this plan. Null if the plan has no trial period.'
        )
    )
    statement_descriptor = models.CharField(
        max_length=255,
        help_text=(
            'Extra information about a charge for the customer’s credit card '
            'statement.'
        )
    )


COUPON_DURATION_CHOICES = (
    ('FOREVER', 'forever'),
    ('ONCE', 'once'),
    ('REPREATING', 'repeating'),
)


class Coupon(models.Model):

    """Stipe Coupon object.

    A coupon contains information about a percent-off or amount-off discount
    you might want to apply to a customer. Coupons only apply to invoices; they
    do not apply to one-off charges.
    """

    livemode = models.BooleanField()
    created = models.DateTimeField()
    duration = models.CharField(
        max_length=255,
        choices=COUPON_DURATION_CHOICES,
        help_text=_(
            'One of ``forever``, ``once``, and ``repeating``. Describes how '
            'long a customer who applies this coupon will get the discount.'
        )
    )
    amount_off = models.PositiveIntegerField(
        help_text=_(
            'Amount (in the ``currency`` specified) that will be taken off '
            'the subtotal of any invoices for this customer.'
        )
    )
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_(
            'If ``amount_off`` has been set, the currency of the amount to '
            'take off.'
        )
    )
    duration_in_months = models.PositiveIntegerField(
        help_text=_(
            'If ``duration`` is ``repeating``, the number of months the '
            'coupon applies. Null if coupon ``duration`` is ``forever``'
            'or ``once``.'
        )
    )
    max_redemptions = models.PositiveIntegerField(
        help_text=_(
            'Maximum number of times this coupon can be redeemed, in total, '
            'before it is no longer valid.'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'coupon in a structured format.'
        )
    )
    percent_off = models.PositiveIntegerField(
        help_text=_(
            'Percent that will be taken off the subtotal of any invoices for '
            'this customer for the duration of the coupon. For example, a '
            'coupon with percent_off of 50 will make a $100 invoice $50 '
            'instead.'
        )
    )
    redeem_by = models.DateTimeField(
        help_text=_(
            'Date after which the coupon can no longer be redeemed'
        )
    )
    times_redeemed = models.PositiveIntegerField(
        help_text=_(
            'Number of times this coupon has been applied to a customer.'
        )
    )
    valid = models.BooleanField(
        help_text=_(
            'Taking account of the above properties, whether this coupon can '
            'still be applied to a customer'
        )
    )


class Discount(models.Model):

    """Stripe Discount object.

    A discount represents the actual application of a coupon to a particular
    customer. It contains information about when the discount began and when it
    will end.
    """

    coupon = models.ForeignKey(
        'Coupon',
        help_text=_(
            'Hash describing the coupon applied to create this discount',
        ),
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    start = models.DateTimeField(
        help_text=_('Date that the coupon was applied')
    )
    end = models.DateTimeField(
        help_text=_(
            'If the coupon has a duration of ``once`` or ``repeating``, the '
            'date that this discount will end. If the coupon used has a '
            'forever duration, this attribute will be null.'
        )
    )
    # subscription = models.ForeignKey(
    #     'Subscription',
    #     help_text=_(
    #         'The subscription that this coupon is applied to, if it is '
    #         'applied to a particular subscription'
    #     )
    # )


class Invoice(models.Model):

    """Stripe Invoice object.

    Invoices are statements of what a customer owes for a particular billing
    period, including subscriptions, invoice items, and any automatic proration
    adjustments if necessary.

    Once an invoice is created, payment is automatically attempted. Note that
    the payment, while automatic, does not happen exactly at the time of
    invoice creation. If you have configured webhooks, the invoice will wait
    until one hour after the last webhook is successfully sent (or the last
    webhook times out after failing).

    Any customer credit on the account is applied before determining how much
    is due for that invoice (the amount that will be actually charged). If the
    amount due for the invoice is less than 50 cents (the minimum for a
    charge), We add the amount to the customer's running account balance to be
    added to the next invoice. If this amount is negative, it will act as a
    credit to offset the next invoice. Note that the customer account balance
    does not include unpaid invoices; it only includes balances that need to be
    taken into account when calculating the amount due for the next invoice.
    """

    livemode = models.BooleanField()
    amount_due = models.IntegerField(
        help_text=_(
            'Final amount due at this time for this invoice. If the invoice’s '
            'total is smaller than the minimum charge amount, for example, or '
            'if there is account credit that can be applied to the invoice, '
            'the ``amount_due`` may be 0. If there is a positive '
            '``starting_balance`` for the invoice (the customer owes money), '
            'the amount_due will also take that into account. The charge that '
            'gets generated for the invoice will be for the amount specified '
            'in amount_due.'
        )
    )
    attempt_count = models.PositiveIntegerField(
        help_text=_(
            'Number of payment attempts made for this invoice, from the '
            'perspective of the payment retry schedule. Any payment attempt '
            'counts as the first attempt, and subsequently only automatic '
            'retries increment the attempt count. In other words, manual '
            'payment attempts after the first attempt do not affect the '
            'retry schedule.'
        )
    )
    attempted = models.BooleanField(
        help_text=_(
            'Whether or not an attempt has been made to pay the invoice. An '
            'invoice is not attempted until 1 hour after the '
            '``invoice.created`` webhook, for example, so you might not want '
            'to display that invoice as unpaid to your users.'
        )
    )
    closed = models.BooleanField(
        help_text=_(
            'Whether or not the invoice is still trying to collect payment. '
            'An invoice is closed if it’s either paid or it has been marked '
            'closed. A closed invoice will no longer attempt to collect '
            'payment.'
        )
    )
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES
    )
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,)
    date = models.DateTimeField()
    forgiven = models.BooleanField(
        help_text=_(
            'Whether or not the invoice has been forgiven. Forgiving an '
            'invoice instructs us to update the subscription status as if the '
            'invoice were succcessfully paid. Once an invoice has been '
            'forgiven, it cannot be unforgiven or reopened'
        )
    )
    lines = json.JSONField(
        help_text=_(
            'The individual line items that make up the invoice. ``lines`` is '
            'sorted as follows: invoice items in reverse chronological order, '
            'followed by the subscription, if any.'
        )
    )
    paid = models.BooleanField(
        help_text=_(
            'Whether or not payment was successfully collected for this '
            'invoice. An invoice can be paid (most commonly) with a charge or '
            'with credit from the customer’s account balance.'
        )
    )
    period_end = models.DateTimeField(
        help_text=_(
            'End of the usage period during which invoice items were added to '
            'this invoice'
        )
    )
    period_start = models.DateTimeField(
        help_text=_(
            'Start of the usage period during which invoice items were added '
            'to this invoice'
        )
    )
    starting_balance = models.IntegerField(
        help_text=_(
            'Starting customer balance before attempting to pay invoice. If '
            'the invoice has not been attempted yet, this will be the current '
            'customer balance.'
        )
    )
    subtotal = models.IntegerField(
        help_text=_(
            'Total of all subscriptions, invoice items, and prorations on the '
            'invoice before any discount is applied'
        )
    )
    total = models.IntegerField(
        help_text=_(
            'Total after discount'
        )
    )
    application_fee = models.IntegerField(
        help_text=_(
            'The fee in cents that will be applied to the invoice and '
            'transferred to the application owner’s Stripe account when the '
            'invoice is paid.'
        )
    )
    # Reverse
    # charge = models.ForeignKey(
    #     'Charge',
    #     help_text=_(
    #         'ID of the latest charge generated for this invoice, if any.'
    #     )
    # )
    description = models.CharField(max_length=255)
    discount = models.ForeignKey('Discount', on_delete=models.CASCADE,)
    ending_balance = models.IntegerField(
        help_text=_(
            'Ending customer balance after attempting to pay invoice. If the '
            'invoice has not been attempted yet, this will be null.'
        )
    )
    next_payment_attempt = models.DateTimeField(
        help_text=_(
            'The time at which payment will next be attempted.'
        )
    )
    receipt_number = models.CharField(
        max_length=255,
        help_text=_(
            'This is the transaction number that appears on email receipts '
            'sent for this invoice.'
        )
    )
    statement_descriptor = models.CharField(
        max_length=255,
        help_text=_(
            'Extra information about an invoice for the customer’s credit '
            'card statement.'
        )
    )
    subscription = models.ForeignKey(
        'Subscription',
        help_text=_(
            'The subscription that this invoice was prepared for, if any.',
        ),
        on_delete=models.CASCADE,
    )
    webhooks_delivered_at = models.DateTimeField(
        help_text=_(
            'The time at which webhooks for this invoice were successfully '
            'delivered (if the invoice had no webhooks to deliver, this will '
            'match ``date``). Invoice payment is delayed until webhooks are '
            'delivered, or until all webhook delivery attempts have been '
            'exhausted.'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'invoice in a structured format.'
        )
    )
    subscription_proration_date = models.IntegerField(
        help_text=_(
            'Only set for upcoming invoices that preview prorations. The time '
            'used to calculate prorations.'
        )
    )
    tax = models.IntegerField(
        help_text=_(
            'The amount of tax included in the total, calculated from '
            '``tax_percent`` and the subtotal. If no ``tax_percent`` is '
            'defined, this value will be null.'
        )
    )
    tax_percent = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text=_(
            'This percentage of the subtotal has been added to the total '
            'amount of the invoice, including invoice line items and '
            'discounts. This field is inherited from the subscription’s '
            '``tax_percent`` field, but can be changed before the invoice is '
            'paid. This field defaults to null.'
        )
    )


class InvoiceItem(models.Model):

    """Stripe Invoice Item object.

    Sometimes you want to add a charge or credit to a customer but only
    actually charge the customer's card at the end of a regular billing
    cycle. This is useful for combining several charges to minimize
    per-transaction fees or having Stripe tabulate your usage-based
    billing totals.
    """

    livemode = models.BooleanField()
    amount = models.IntegerField()
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES
    )
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,)
    date = models.DateTimeField()
    discountable = models.BooleanField(
        help_text=_(
            'If true, discounts will apply to this invoice item. Always false '
            'for prorations.'
        )
    )
    proration = models.BooleanField(
        help_text=_(
            'Whether or not the invoice item was created automatically as a '
            'proration adjustment when the customer switched plans'
        )
    )
    description = models.CharField(
        max_length=255
    )
    invoice = models.CharField(max_length=255)
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'invoice item in a structured format.'
        )
    )
    period = json.JSONField()
    plan = models.ForeignKey(
        'Plan',
        help_text=_(
            'If the invoice item is a proration, the plan of the subscription '
            'that the proration was computed for.',
        ),
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        help_text=_(
            'If the invoice item is a proration, the quantity of the '
            'subscription that the proration was computed for.'
        )
    )
    subscription = models.ForeignKey(
        'Subscription',
        help_text=_(
            'The subscription that this invoice item has been created for, if '
            'any.',
        ),
        on_delete=models.CASCADE,
    )


class Dispute(models.Model):

    """Stripe Dispute object.

    A dispute occurs when a customer questions your charge with their bank or
    credit card company. When a customer disputes your charge, you're given the
    opportunity to respond to the dispute with evidence that shows the charge
    is legitimate. You can find more information about the dispute process in
    our disputes FAQ.
    """

    livemode = models.BooleanField()
    amount = models.IntegerField(
        help_text=_(
            'Disputed amount. Usually the amount of the charge, but can '
            'differ (usually because of currency fluctuation or because only '
            'part of the order is disputed).'
        )
    )
    # reverse
    # charge = models.ForeignKey(
    #     'Charge',
    #     help_text=_('ID of the charge that was disputed')
    # )
    created = models.DateTimeField(
        help_text=_('Date dispute was opened')
    )
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'Three-letter ISO currency code representing the currency of the '
            'amount that was disputed. '
        )
    )
    reason = models.CharField(
        max_length=255,
        help_text=_(
            'Reason given by cardholder for dispute. Possible values are '
            '``duplicate``, ``fraudulent``, ``subscription_canceled``, '
            '``product_unacceptable``, ``product_not_received``, '
            '``unrecognized``, ``credit_not_processed``, ``general``. Read '
            'more about dispute reasons.'
        )
    )
    status = models.CharField(
        max_length=255,
        help_text=_(
            'Current status of dispute. Possible values are '
            '``warning_needs_response``, ``warning_under_review``, '
            '``warning_closed``, ``needs_response``, ``response_disabled``, '
            '``under_review``, ``charge_refunded``, ``won``, ``lost``.'
        )
    )
    balance_transaction = models.ManyToManyField(
        'BalanceTransaction',
        help_text=_(
            'List of zero, one, or two balance transactions that show funds '
            'withdrawn and reinstated to your Stripe account as a result of '
            'this dispute.'
        )
    )
    evidence = models.ForeignKey(
        'DisputeEvidence',
        help_text=_(
            'Evidence provided to respond to a dispute. Updating any field in '
            'the hash will submit all fields in the hash for review.',
        ),
        on_delete=models.CASCADE,
    )
    evidence_details = json.JSONField(
        help_text=_(
            'Information about the evidence submission.'
        )
    )
    is_charge_refundable = models.BooleanField(
        'If true, it is still possible to refund the disputed payment. Once '
        'the payment has been fully refunded, no further funds will be '
        'withdrawn from your Stripe account as a result of this dispute.'
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'dispute in a structured format.'
        )
    )


class DisputeEvidence(models.Model):

    """Stripe Dispute Evidence object.

    :class:`DisputeEvidence` revserse relations will be prefixed with
    ``dispute_``.
    """

    access_activity_log = models.TextField(
        help_text=_(
            'Any server or activity logs showing proof that the customer '
            'accessed or downloaded the purchased digital product. This '
            'information should include IP addresses, corresponding '
            'timestamps, and any detailed recorded activity.'
        )
    )
    billing_address = models.TextField(
        help_text=_(
            'The billing addess provided by the customer.'
        )
    )
    cancelling_policy = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Your subscription cancellation policy, as '
            'shown to the customer.'
        ),
        related_name='dispute_cancelling_policy',
        on_delete=models.CASCADE,
    )
    cancellation_policy_disclosure = models.TextField(
        help_text=_(
            'An explanation of how and when the customer was shown your '
            'refund policy prior to purchase.'
        )
    )
    cancellation_rebuttal = models.TextField(
        help_text=_(
            'A justification for why the customer’s subscription was not '
            'canceled.'
        )
    )
    customer_communication = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Any communication with the customer that '
            'you feel is relevant to your case (for example emails proving '
            'that they received the product or service, or demonstrating '
            'their use of or satisfaction with the product or service)'
        ),
        related_name='dispute_customer_communication',
        on_delete=models.CASCADE,
    )
    customer_email_address = models.EmailField()
    customer_name = models.CharField(max_length=255)
    customer_purchase_ip = models.CharField(max_length=255)
    customer_signature = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) A relevant document or contract showing '
            'the customer’s signature.',
        ),
        related_name='dispute_customer_signature',
        on_delete=models.CASCADE,
    )
    duplicate_charge_documentation = models.ForeignKey(
        'FileUpload',
        help_text=(
            'ID of a file upload) Documentation for the prior charge that can '
            'uniquely identify the charge, such as a receipt, shipping label, '
            'work order, etc. This document should be paired with a similar '
            'document from the disputed payment that proves the two payments '
            'are separate.'
        ),
        related_name='dispute_charge_documentation',
        on_delete=models.CASCADE,
    )
    duplicate_charge_explanation = models.TextField(
        help_text=_(
            'An explanation of the difference between the disputed charge and '
            'the prior charge that appears to be a duplicate.'
        )
    )
    duplicate_charge_id = models.ForeignKey(
        'Charge',
        help_text=_(
            'The Stripe ID for the prior charge which appears to be a '
            'duplicate of the disputed charge.',
        ),
        related_name='dispute_charge',
        on_delete=models.CASCADE,
    )
    product_description = models.TextField(
        help_text=_(
            'A description of the product or service which was sold.'
        )
    )
    receipt = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Any receipt or message sent to the '
            'customer notifying them of the charge.'
        ),
        related_name='dispute_receipt',
        on_delete=models.CASCADE,
    )
    refund_policy = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Your refund policy, as shown to the '
            'customer.'
        ),
        related_name='dispute_refund_policy',
        on_delete=models.CASCADE,
    )
    refund_policy_disclosure = models.TextField(
        help_text=_(
            'Documentation demonstrating that the customer was shown your '
            'refund policy prior to purchase.'
        )
    )
    refund_refusal_explanation = models.TextField(
        help_text=_(
            'A justification for why the customer is not entitled to a refund.'
        )
    )
    service_date = models.DateTimeField(
        help_text=_(
            'The date on which the customer received or began receiving the '
            'purchased service, in a clear human-readable format.'
        )
    )
    service_documentation = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Documentation showing proof that a service '
            'was provided to the customer. This could include a copy of a '
            'signed contract, work order, or other form of written agreement.'
        ),
        related_name='dispute_service_documentation',
        on_delete=models.CASCADE,
    )
    shipping_address = models.TextField(
        help_text=_(
            'The address to which a physical product was shipped. You should '
            'try to include as much complete address information as possible.'
        )
    )
    shipping_carrier = models.TextField(
        help_text=_(
            'The delivery service that shipped a physical product, such as '
            'Fedex, UPS, USPS, etc. If multiple carriers were used for this '
            'purchase, please separate them with commas.'
        )
    )
    shipping_date = models.DateTimeField(
        help_text=_(
            'The date on which a physical product began its route to the '
            'shipping address, in a clear human-readable format.'
        )
    )
    shipping_documentation = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Documentation showing proof that a product '
            'was shipped to the customer at the same address the customer '
            'provided to you. This could include a copy of the shipment '
            'receipt, shipping label, etc, and should show the full shipping '
            'address of the customer, if possible.'
        ),
        related_name='dispute_shipping_documentation',
        on_delete=models.CASCADE,
    )
    shipping_tracking_number = models.TextField(
        help_text=_(
            'The tracking number for a physical product, obtained from the '
            'delivery service. If multiple tracking numbers were generated '
            'for this purchase, please separate them with commas.'
        )
    )
    uncategorized_file = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Any additional evidence or statements.'
        ),
        related_name='dispute_uncategorized_file',
        on_delete=models.CASCADE,
    )
    uncategorized_text = models.TextField(
        help_text=_('Any additional evidence or statements.')
    )


TRANSFER_STATUS_CHOICES = (
    ('paid', _('Paid')),
    ('canceled', _('Canceled')),
    ('failed', _('Failed')),
)
TRANSFER_TYPE_CHOICES = (
    ('card', _('Card')),
    ('bank_account', _('Bank account')),
    ('stripe_account', _('Stripe account')),
)
TRANSFER_FAILURE_CHOICES = (
    (
        'insufficient_funds', _(
            'Your Stripe account has insufficient funds to cover the transfer.'
        )
    ),
    (
        'account_closed',
        _(
            'The bank account has been closed.'
        )
    ),
    (
        'no_account',
        _(
            'The bank account details on file are probably incorrect. No bank '
            'account could be located with those details.'
        )
    ),
    (
        'invalid_account_number',
        _(
            'The routing number seems correct, but the account number is '
            'invalid.'
        )
    ),
    (
        'debit_not_authorized',
        _(
            'Debit transactions are not approved on the bank account. Stripe '
            'requires bank accounts to be set up for both credit and debit '
            'transfers.'
        )
    ),
    (
        'bank_ownership_changed',
        _(
            'The destination bank account is no longer valid because its '
            'branch has changed ownership.'
        )
    ),
    (
        'account_frozen',
        _('The bank account has been frozen.')
    ),
    (
        'could_not_process',
        _('The bank could not process this transfer.')
    ),
    (
        'bank_account_restricted',
        _(
            'The bank account has restrictions on either the type or number '
            'of transfers allowed. This normally indicates that the bank '
            'account is a savings or other non-checking account.'
        )
    ),
    (
        'invalid_currency',
        _(
            'The bank was unable to process this transfer because of its '
            'currency. This is probably because the bank account cannot '
            'accept payments in that currency.'
        )
    ),
)


class Transfer(models.Model):

    """Stripe Transfer object.

    When Stripe sends you money or you initiate a transfer to a bank account,
    debit card, or connected Stripe account, a transfer object will be created.
    You can retrieve individual transfers as well as list all transfers.

    View the `documentation` on creating transfers via the API.

    .. _documentation: https://stripe.com/docs/tutorials/sending-transfers
    """

    livemode = models.BooleanField()
    amount = models.IntegerField(
        help_text=_(
            'Amount (in cents) to be transferred to your bank account'
        )
    )
    created = models.DateTimeField(
        help_text=_(
            'Time that this record of the transfer was first created.'
        )
    )
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_(
            'Three-letter ISO code representing the currency of the transfer.'
        )
    )
    date = models.DateTimeField(
        help_text=_(
            'Date the transfer is scheduled to arrive in the bank. This '
            'doesn’t factor in delays like weekends or bank holidays.'
        )
    )
    reversals = json.JSONField(
        help_text=_(
            'A list of reversals that have been applied to the transfer.'
        )
    )
    reversed = models.BooleanField(
        help_text=_(
            'Whether or not the transfer has been fully reversed. If the '
            'transfer is only partially reversed, this attribute will still '
            'be false.'
        )
    )

    status = models.CharField(
        max_length=255,
        help_text=_(
            'Current status of the transfer (``paid``, ``pending``, '
            '``canceled`` or ``failed``). A transfer will be ``pending`` '
            'until it is submitted, at which point it becomes ``paid``. If it '
            'does not go through successfully, its status will change to '
            '``failed`` or ``canceled``.'
        ),
        choices=TRANSFER_STATUS_CHOICES
    )
    type = models.CharField(
        max_length=255,
        help_text=_(
            'The type of this type of this transfer. Can be ``card``, '
            '``bank_account``, or ``stripe_account``.'
        ),
        choices=TRANSFER_TYPE_CHOICES
    )
    amount_reversed = models.IntegerField(
        help_text=_(
            'Amount in cents reversed (can be less than the amount attribute '
            'on the transfer if a partial reversal was issued).'
        )
    )
    balance_transaction = models.ForeignKey(
        'BalanceTransaction',
        help_text=_(
            'Balance transaction that describes the impact of this transfer '
            'on your account balance.',
        ),
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        help_text=_(
            'Internal-only description of the transfer'
        )
    )
    failure_code = models.CharField(
        max_length=255,
        help_text=_(
            'Error code explaining reason for transfer failure if available. '
            'See Types of transfer failures for a list of failure codes.'
        ),
        choices=TRANSFER_FAILURE_CHOICES
    )
    failure_message = models.TextField(
        help_text=_(
            'Message to user further explaining reason for transfer failure '
            'if available.'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'transfer in a structured format.'
        )
    )
    application_fee = models.CharField(max_length=255)
    destination = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the bank account, card, or Stripe account the transfer was '
            'sent to.'
        )
    )
    destination_payment = models.CharField(
        max_length=255,
        help_text=_(
            'If the destination is a Stripe account, this will be the ID of '
            'the payment that the destination account received for the '
            'transfer.'
        )
    )
    source_transaction = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the charge (or other transaction) that was used to fund '
            'the transfer. If null, the transfer was funded from the '
            'available balance.'
        )
    )
    statement_descriptor = models.CharField(
        max_length=255,
        help_text=_(
            'Extra information about a transfer to be displayed on the user’s '
            'bank statement.'
        )
    )


class TransferReversal(models.Model):

    """Stripe Transfer Reversal object.

    A previously created transfer can be reversed if it has not yet been paid
    out. Funds will be refunded to your available balance, and the fees you
    were originally charged on the transfer will be refunded. You may not
    reverse automatic Stripe transfers.
    """

    amount = models.IntegerField(
        help_text=_(
            'Amount reversed, in cents.'
        )
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES,
        help_text=_(
            'Three-letter ISO code representing the currency of the reversal.'
        )
    )
    balance_transaction = models.ForeignKey(
        'BalanceTransaction',
        help_text=_(
            'Balance transaction that describes the impact of this reversal '
            'on your account balance.'
        ),
        related_name='transfer_reversal_balance_transaction',
        on_delete=models.CASCADE,
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'transfer reversal in a structured format.'
        )
    )
    transfer = models.ForeignKey(
        'Transfer',
        help_text=_(
            'ID of the transfer that was reversed.'
        ),
        on_delete=models.CASCADE,
    )


RECIPIENT_TYPE_CHOICES = (
    ('individual', _('Individual')),
    ('corporoation', _('Corporation')),
)


class Recipient(models.Model):

    """Stripe Recipient object.

    With recipient objects, you can transfer money from your Stripe account to
    a third party bank account or debit card. The API allows you to create,
    delete, and update your recipients. You can retrieve individual recipients
    as well as a list of all your recipients.

    Recipient objects have been deprecated in favor of Connect, specifically
    the much more powerful account objects. Please use them instead. If you are
    already using recipients, please see our migration guide for more
    information.
    """

    livemode = models.BooleanField()
    created = models.DateTimeField()
    type = models.CharField(
        max_length=255,
        help_text=_(
            'Type of the recipient, one of ``individual`` or ``corporation``.'
        ),
        choices=RECIPIENT_TYPE_CHOICES
    )
    active_account = json.JSONField(
        help_text=_(
            'Hash describing the current account on the recipient, if there '
            'is one.'
        )
    )
    description = models.TextField()
    email = models.EmailField()
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'recipient in a structured format.'
        )
    )
    name = models.CharField(
        max_length=255,
        help_text=_('Full, legal name of the recipient.')
    )
    cards = models.ManyToManyField('Card', related_name='recipients')
    default_card = models.ForeignKey(
        'Card',
        help_text=_(
            'The default card to use for creating transfers to this recipient.'
        ),
        related_name='recipients_default',
        on_delete=models.CASCADE,
    )
    migrated_to = models.CharField(max_length=255)


class ApplicationFee(models.Model):

    """Stripe Application Fee object.

    When you collect a transaction fee on top of a charge made for your user
    (using Stripe Connect), an application fee object is created in your
    account. You can list, retrieve, and refund application fees.

    For more information on collecting transaction fees, see our documentation.
    """

    livemode = models.BooleanField()
    account = models.ForeignKey(
        'Account',
        help_text=_(
            'ID of the Stripe account this fee was taken from.',
        ),
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        help_text=_(
            'Amount earned, in cents.'
        )
    )
    application = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the Connect Application that earned the fee.'
        )
    )
    balance_transaction = models.ForeignKey(
        'BalanceTransaction',
        help_text=_(
            'Balance transaction that describes the impact of this collected '
            'application fee on your account balance (not including refunds).'
        ),
        on_delete=models.CASCADE,
    )
    charge = models.ForeignKey(
        'Charge',
        help_text=_(
            'ID of the charge that the application fee was taken from.'
        ),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'Three-letter ISO currency code representing the currency of the'
            'charge.'
        ),
        choices=CURRENCY_CHOICES
    )
    refunded = models.BooleanField(
        help_text=_(
            'Whether or not the fee has been fully refunded. If the fee is '
            'only partially refunded, this attribute will still be false.'
        )
    )
    # refunds reverse relation from 'Refund'
    amount_refunded = models.PositiveIntegerField()


class ApplicationFeeRefund(models.Model):

    """Stripe Application Fee Refund object.

    Application Fee Refund objects allow you to refund an application fee that
    has previously been created but not yet refunded. Funds will be refunded to
    the Stripe account that the fee was originally collected from.
    """

    amount = models.IntegerField(
        help_text=_('Amount reversed, in cents.')
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'Three-letter ISO currency code representing the currency of the '
            'reverse.'
        ),
        choices=CURRENCY_CHOICES
    )
    balance_transaction = models.ForeignKey(
        'BalanceTransaction',
        help_text=_(
            'Balance transaction that describes the impact of this reversal '
            'on your account balance.'
        ),
        on_delete=models.CASCADE,
    )
    fee = models.ForeignKey(
        'ApplicationFee',
        help_text=_(
            'ID of the application fee that was refunded.'
        ),
        on_delete=models.CASCADE,
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'charge in a structured format.'
        )
    )


class Account(models.Model):

    """Stripe Account object.

    This is an object representing your Stripe account. You can retrieve it to
    see properties on the account like its current e-mail address or if the
    account is enabled yet to make live charges.

    Some properties, marked as 'managed accounts only', are only available to
    platforms who want to create and manage Stripe accounts.
    """

    charges_enabled = models.BooleanField(
        help_text=_(
            'Whether or not the account can create live charges'
        )
    )
    country = models.CharField(  # todo: add CHOICES
        max_length=255,
        help_text=_('The country of the account')
    )
    currencies_supports = json.JSONField(
        help_text=_(
            'The currencies this account can submit when creating charges'
        )
    )
    default_currency = models.CharField(
        max_length=255,
        help_text=_(
            'The currency this account has chosen to use as the default'
        ),
        choices=CURRENCY_CHOICES
    )
    details_submitted = models.BooleanField(
        help_text=_(
            'Whether or not account details have been submitted yet. '
            'Standalone accounts cannot receive transfers before this is true.'
        )
    )
    transfers_enabled = models.BooleanField(
        help_text=_(
            'Whether or not Stripe will send automatic transfers for this '
            'account. This is only false when Stripe is waiting for '
            'additional information from the account holder.'
        )
    )
    display_name = models.CharField(
        max_length=255,
        help_text=_(
            'The display name for this account. This is used on the Stripe '
            'dashboard to help you differentiate between accounts.'
        )
    )
    email = models.EmailField(
        help_text=_('The primary user’s email address')
    )
    statement_descriptor = models.TextField(
        help_text=_('The text that will appear on credit card statements')
    )
    timezone = models.CharField(
        max_length=255,
        help_text=_(
            'The timezone used in the Stripe dashboard for this account. A '
            'list of possible timezone values is maintained at the IANA '
            'Timezone Database.'
        )
    )
    business_name = models.CharField(
        max_length=255,
        help_text=_(
            'The publicly visible name of the business'
        )
    )
    business_url = models.URLField(
        help_text=_(
            'The publicly visible website of the business'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'charge in a structured format.'
        )
    )
    support_phone = models.CharField(
        max_length=255,
        help_text=_(
            'The publicly visible support phone number for the business'
        )
    )
    managed = models.BooleanField(
        help_text=_(
            'Whether or not the account is managed by your platform. Returns '
            'null if the account was not created by a platform.'
        )
    )
    bank_accounts = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'Bank accounts currently attached to this account.'
        )
    )
    debit_negative_balances = models.BooleanField(
        help_text=_(
            '(Managed Accounts Only) '
            'Whether or not Stripe will attempt to reclaim negative account '
            'balances from this account’s bank account.'
        )
    )
    decline_charge_on = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'Account-level settings to automatically decline certain types of '
            'charges regardless of the bank’s decision.'
        )
    )
    legal_entity = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'Information regarding the owner of this account, including '
            'verification status.'
        )
    )
    product_description = models.TextField(
        help_text=_(
            '(Managed Accounts Only) '
            'An internal-only description of the product or service provided. '
            'This is used by Stripe in the event the account gets flagged for '
            'potential fraud.'
        )
    )
    tos_acceptance = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'Who accepted the Stripe terms of service, and when they accepted '
            'it.'
        )
    )
    transfer_schedule = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'When payments collected will be automatically paid out to the '
            'account holder’s bank account'
        )
    )
    verfication = json.JSONField(
        help_text=_(
            '(Managed Accounts Only) '
            'That state of the account’s information requests, including what '
            'information is needed and by when it must be provided.'
        )
    )


class Balance(models.Model):

    """Stripe Balance object.

    This is an object representing your Stripe balance. You can retrieve it to
    see the balance currently on your Stripe account.

    You can also retrieve a list of the balance history, which contains a full
    list of transactions that have ever contributed to the balance (charges,
    refunds, transfers, and so on).
    """

    livemode = models.BooleanField()
    available = json.JSONField(
        help_text=(
            'Funds that are available to be paid out automatically by Stripe '
            'or explicitly via the transfers API.'
        )
    )
    pending = json.JSONField(
        help_text=_(
            'Funds that are not available in the balance yet, due to the '
            '7-day rolling pay cycle.'
        )
    )


class BalanceTransaction(models.Model):
    amount = models.IntegerField(
        help_text=_(
            'Gross amount of the transaction, in cents'
        )
    )
    available_on = models.DateTimeField(
        help_text=_(
            'The date the transaction’s net funds will become available in '
            'the Stripe balance.'
        )
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        choices=CURRENCY_CHOICES
    )
    fee = models.IntegerField(
        help_text=_(
            'Fees (in cents) paid for this transaction'
        )
    )
    fee_details = json.JSONField(
        help_text=_(
            'Detailed breakdown of fees (in cents) paid for this transaction'
        )
    )
    net = models.IntegerField(
        help_text=_(
            'Net amount of the transaction, in cents.'
        )
    )
    status = models.CharField(
        max_length=255,
        help_text=_(
            'If the transaction’s net funds are available in the Stripe '
            'balance yet. Either ``available`` or ``pending``.'
        )
    )
    type = models.CharField(
        max_length=255,
        help_text=_(
            'Type of the transaction, one of: ``charge``, ``refund``, '
            '``adjustment``, ``application_fee``, ``application_fee_refund``, '
            '``transfer``, ``transfer_cancel`` or ``transfer_failure``.'
        )
    )
    description = models.CharField(max_length=255)
    source = json.JSONField(
        help_text=_(
            'The Stripe object this transaction is related to.'
        )
    )
    sourced_transfers = json.JSONField(
        help_text=_(
            'The transfers (if any) for which source is a source_transaction.'
        )
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

    livemode = models.BooleanField()
    created = models.DateTimeField()
    data = json.JSONField(
        help_text=_(
            'Hash containing data associated with the event.'
        )
    )
    pending_webhooks = models.PositiveIntegerField(
        help_text=_(
            'Number of webhooks yet to be delivered successfully (return a '
            '20x response) to the URLs you’ve specified.'
        )
    )
    type = models.CharField(
        max_length=255,
        help_text=_(
            'Description of the event: e.g. invoice.created, charge.refunded, '
            'etc.'
        )
    )
    api_version = models.CharField(
        max_length=255,
        help_text=_(
            'The Stripe API version used to render data. Note: this property '
            'is populated for events on or after October 31, 2014.'
        )
    )
    request = models.CharField(
        max_length=255,
        help_text=_(
            'ID of the API request that caused the event. If null, the event '
            'was automatic (e.g. Stripe’s automatic subscription handling). '
            'Request logs are available in the dashboard but currently not in '
            'the API. Note: this property is populated for events on or after '
            'April 23, 2013.'
        )
    )


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

    livemode = models.BooleanField()
    created = models.DateTimeField()
    type = models.CharField(
        max_length=255,
        choices=TOKEN_TYPE_CHOICES,
        help_text=_(
            'Type of the token: ``card`` or ``bank_account``'
        )
    )
    used = models.BooleanField(
        help_text=_(
            'Whether or not this token has already been used (tokens can be '
            'used only once)'
        )
    )
    bank_account = json.JSONField(
        help_text=_('Hash describing the bank account')
    )
    card = json.JSONField(
        help_text=_('Hash describing the bank account')
    )
    client_ip = models.CharField(
        max_length=255,
        help_text=_(
            'IP address of the client that generated the token'
        )
    )


class BitCoinReceiver(models.Model):

    """Stripe Bitcoin Receiver object.

    A Bitcoin receiver wraps a Bitcoin address so that a customer can push a
    payment to you. This `guide`_ describes how to use receivers to create
    Bitcoin payments.

    .. _guide: https://stripe.com/docs/guides/bitcoin
    """

    livemode = models.BooleanField()
    active = models.BooleanField(
        help_text=_(
            'True when this bitcoin receiver has received a non-zero amount '
            'of bitcoin.'
        )
    )
    amount = models.PositiveIntegerField(
        help_text=_(
            'The amount of currency that you are collecting as payment.'
        )
    )
    amount_received = models.PositiveIntegerField(
        help_text=_(
            'The amount of currency to which bitcoin_amount_received has been '
            'converted.'
        )
    )
    bitcoin_amount = models.PositiveIntegerField(
        help_text=_(
            'The amount of bitcoin that the customer should send to fill the '
            'receiver. The bitcoin_amount is denominated in Satoshi: there '
            'are 10^8 Satoshi in one bitcoin.'
        )
    )
    bitcoin_amount_received = models.PositiveIntegerField(
        help_text=_(
            'The amount of bitcoin that has been sent by the customer to this '
            'receiver.'
        )
    )
    bitcoin_uri = models.URLField(
        help_text=_(
            'This URI can be displayed to the customer as a clickable link '
            '(to activate their bitcoin client) or as a QR code (for mobile '
            'wallets).'
        )
    )
    created = models.DateTimeField()
    currency = models.CharField(
        max_length=255,
        help_text=_(
            'Three-letter ISO currency code representing the currency to '
            'which the bitcoin will be converted.'
        ),
        choices=CURRENCY_CHOICES
    )
    filled = models.BooleanField(
        help_text=_(
            'This flag is initially false and updates to true when the '
            'customer sends the bitcoin_amount to this receiver.'
        )
    )
    inbound_address = models.CharField(
        max_length=255,
        help_text=_(
            'A bitcoin address that is specific to this receiver. The '
            'customer can send bitcoin to this address to fill the receiver.'
        )
    )
    transactions = json.JSONField(
        help_text=_(
            'A list with one entry for each time that the customer sent '
            'bitcoin to the receiver. Hidden when viewing the receiver with a '
            'publishable key.'
        )
    )
    uncaptured_funds = models.BooleanField(
        help_text=_(
            'This receiver contains uncaptured funds that can be used for a '
            'payment or refunded.'
        )
    )
    description = models.CharField(max_length=255)
    email = models.EmailField(
        help_text=_(
            'The customer’s email address, set by the API call that creates '
            'the receiver.'
        )
    )
    metadata = json.JSONField(
        help_text=_(
            'A set of key/value pairs that you can attach to a charge object. '
            'it can be useful for storing additional information about the '
            'charge in a structured format.'
        )
    )
    payment = models.CharField(
        max_length=255,
        help_text=_(
            'The ID of the payment created from the receiver, if any. Hidden '
            'when viewing the receiver with a publishable key.'
        )
    )
    refund_address = models.CharField(
        max_length=255,
        help_text=_(
            'The refund address for these bitcoin, if communicated by the '
            'customer.'
        )
    )
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE,)


FILE_UPLOAD_PURPOSE_CHOICES = (
    ('identity document', _('Identity document')),
    ('dispute_evidence', _('Dispute evidence')),
)


class FileUpload(models.Model):
    created = models.DateTimeField()
    purpose = models.CharField(
        max_length=255,
        help_text=(
            'The purpose of the uploaded file. Possible values are '
            '``identity_document``, ``dispute_evidence``.'
        ),
        choices=FILE_UPLOAD_PURPOSE_CHOICES
    )
    size = models.IntegerField(
        help_text=_(
            'The size in bytes of the file upload object.'
        )
    )
    type = models.CharField(
        max_length=255,
        help_text=_(
            'The type of the file returned. Returns one of the following: '
            '``pdf``, ``jpg``, ``png``.'
        )
    )
    url = models.URLField(
        help_text=_(
            'A read-only URL where the uploaded file can be accessed. Will be '
            'nil unless the uploaded file has one of the following purposes: '
            '``dispute_evidence``. Also nil if retrieved with the publishable '
            'API key.'
        )
    )
