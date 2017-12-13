# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
            'timestamps, and any detailed recorded activity.',
        ),
    )
    billing_address = models.TextField(
        help_text=_(
            'The billing addess provided by the customer.',
        ),
    )
    cancelling_policy = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Your subscription cancellation policy, as '
            'shown to the customer.',
        ),
        related_name='dispute_cancelling_policy',
        on_delete=models.CASCADE,
    )
    cancellation_policy_disclosure = models.TextField(
        help_text=_(
            'An explanation of how and when the customer was shown your '
            'refund policy prior to purchase.',
        ),
    )
    cancellation_rebuttal = models.TextField(
        help_text=_(
            'A justification for why the customer’s subscription was not '
            'canceled.',
        ),
    )
    customer_communication = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Any communication with the customer that '
            'you feel is relevant to your case (for example emails proving '
            'that they received the product or service, or demonstrating '
            'their use of or satisfaction with the product or service)',
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
            'are separate.',),
        related_name='dispute_charge_documentation',
        on_delete=models.CASCADE,
    )
    duplicate_charge_explanation = models.TextField(
        help_text=_(
            'An explanation of the difference between the disputed charge and '
            'the prior charge that appears to be a duplicate.',
        ),
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
            'A description of the product or service which was sold.',
        ),
    )
    receipt = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Any receipt or message sent to the '
            'customer notifying them of the charge.',
        ),
        related_name='dispute_receipt',
        on_delete=models.CASCADE,
    )
    refund_policy = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Your refund policy, as shown to the '
            'customer.',
        ),
        related_name='dispute_refund_policy',
        on_delete=models.CASCADE,
    )
    refund_policy_disclosure = models.TextField(
        help_text=_(
            'Documentation demonstrating that the customer was shown your '
            'refund policy prior to purchase.',
        ),
    )
    refund_refusal_explanation = models.TextField(
        help_text=_(
            'A justification for why the customer is not entitled to a refund.',
        ),
    )
    service_date = models.DateTimeField(
        help_text=_(
            'The date on which the customer received or began receiving the '
            'purchased service, in a clear human-readable format.',
        ),
    )
    service_documentation = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Documentation showing proof that a service '
            'was provided to the customer. This could include a copy of a '
            'signed contract, work order, or other form of written agreement.',
        ),
        related_name='dispute_service_documentation',
        on_delete=models.CASCADE,
    )
    shipping_address = models.TextField(
        help_text=_(
            'The address to which a physical product was shipped. You should '
            'try to include as much complete address information as possible.',
        ),
    )
    shipping_carrier = models.TextField(
        help_text=_(
            'The delivery service that shipped a physical product, such as '
            'Fedex, UPS, USPS, etc. If multiple carriers were used for this '
            'purchase, please separate them with commas.',
        ),
    )
    shipping_date = models.DateTimeField(
        help_text=_(
            'The date on which a physical product began its route to the '
            'shipping address, in a clear human-readable format.',
        ),
    )
    shipping_documentation = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Documentation showing proof that a product '
            'was shipped to the customer at the same address the customer '
            'provided to you. This could include a copy of the shipment '
            'receipt, shipping label, etc, and should show the full shipping '
            'address of the customer, if possible.',
        ),
        related_name='dispute_shipping_documentation',
        on_delete=models.CASCADE,
    )
    shipping_tracking_number = models.TextField(
        help_text=_(
            'The tracking number for a physical product, obtained from the '
            'delivery service. If multiple tracking numbers were generated '
            'for this purchase, please separate them with commas.',
        ),
    )
    uncategorized_file = models.ForeignKey(
        'FileUpload',
        help_text=_(
            '(ID of a file upload) Any additional evidence or statements.',
        ),
        related_name='dispute_uncategorized_file',
        on_delete=models.CASCADE,
    )
    uncategorized_text = models.TextField(
        help_text=_(
            'Any additional evidence or statements.',
        ),
    )
