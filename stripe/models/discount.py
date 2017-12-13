# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
        help_text=_(
            'Date that the coupon was applied',
        ),
    )
    end = models.DateTimeField(
        help_text=_(
            'If the coupon has a duration of ``once`` or ``repeating``, the '
            'date that this discount will end. If the coupon used has a '
            'forever duration, this attribute will be null.',
        ),
    )

    # subscription = models.ForeignKey(
    #     'Subscription',
    #     help_text=_(
    #         'The subscription that this coupon is applied to, if it is '
    #         'applied to a particular subscription'
    #     )
    # )
