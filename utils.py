# -*- coding: utf-8 -*-
import datetime

from django.apps import apps
from django.db import models

import pytz
import stripe


class UnixDateTimeField(models.DateTimeField):

    """Stripe returns date fields in UNIX time epoc as an int"""

    def pre_save(self, model_instance, add):
        if not self.auto_now:
            value = getattr(model_instance, self.attname)
            if isinstance(value, int):
                new_value = datetime.datetime.fromtimestamp(value).replace(
                    tzinfo=pytz.utc,
                )
                setattr(model_instance, self.attname, new_value)
        return super().pre_save(model_instance, add)


def get_customer_info(_dict, customer):
    """Fill in customer info inn from_stripe_object

    This is specialized for the "_dict" convention passed around in
    from_stripe_object.
    """
    Customer = apps.get_model('stripe.Customer')
    # Handle situations like Charge where customer is optional
    customer_id = None
    if 'customer' in _dict:
        customer_id = _dict.pop('customer')

    if customer:
        _dict['customer'] = customer
    elif customer_id:
        customer_object = stripe.Customer.retrieve(customer_id)
        _dict['customer'] = Customer.from_stripe_object(
            customer_object,
            descend=False,
        )
    return _dict
