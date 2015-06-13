# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import Charge
from .helpers import get_test_data


class TestCharge(TestCase):

    def test_create(self):
        data = get_test_data('charge.json')
        print(data)
        c = Charge.objects.create(**data)
