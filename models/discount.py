# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ..utils import UnixDateTimeField, get_customer_info
from .coupon import Coupon


class Discount(models.Model):

    """Stripe Discount object.

    A discount represents the actual application of a coupon to a particular
    customer. It contains information about when the discount began and when it
    will end.
    """

    id = models.CharField(max_length=255, primary_key=True)
    coupon = models.ForeignKey(
        'Coupon',
        help_text=_(
            'Hash describing the coupon applied to create this discount',
        ),
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    start = UnixDateTimeField(help_text=_('Date that the coupon was applied',),)
    end = UnixDateTimeField(
        help_text=_(
            'If the coupon has a duration of ``once`` or ``repeating``, the '
            'date that this discount will end. If the coupon used has a '
            'forever duration, this attribute will be null.',
        ),
        null=True,
    )

    # subscription = models.ForeignKey(
    #     'Subscription',
    #     help_text=_(
    #         'The subscription that this coupon is applied to, if it is '
    #         'applied to a particular subscription'
    #     )
    # )

    @classmethod
    def from_stripe_object(cls, stripe_object, customer=None):
        _dict = stripe_object.to_dict()
        _dict.pop('object')

        _dict['coupon'] = Coupon.from_stripe_object(_dict.pop('coupon'))
        _dict = get_customer_info(_dict, customer)

        s = cls(**_dict)
        s.save()
        return s
