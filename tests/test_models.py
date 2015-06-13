# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from ..models import Customer
from .helpers import get_test_data


class TestCustomer(TestCase):

    def test_create(self):
        data = get_test_data('customer.json')
        print(data)
        c = Customer.objects.create(**data)
