# -*- coding: utf-8 -*-
from django.test import TestCase


class SimpleTestA(TestCase):

    def test_basic_addition(self):
        """that 1 + 1 always equals 2."""
        self.assertEqual(1 + 1, 2)
