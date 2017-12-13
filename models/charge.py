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

CHARGE_FAILURE_CHOICES = ((
    'incorrect_number',
    _('The card number is incorrect'),
),)


class Charge(models.Model):

    """Stripe Charge Object.

    To charge a credit or a debit card, you create a charge object. You can
    retrieve and refund individual charges as well as list all charges. Charges
    are identified by a unique random ID.
    """

    livemode = models.BooleanField(default=True)
    amount = models.IntegerField(help_text=_('Amount charged in cents'),)
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
            'is only partially refunded, this attribute will still be false.',
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
            ' on the charge if a partial refund was issued).',
        ),
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
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=255)
    dispute = models.ForeignKey(
        'Dispute',
        blank=True,
        null=True,
        help_text=_(
            'Details about the dispute if the charge has been disputed.',
        ),
        on_delete=models.CASCADE,
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
        on_delete=models.CASCADE,
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
