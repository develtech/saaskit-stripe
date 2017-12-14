# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

import pytz
from django_extensions.db.fields import json

from .charge import CURRENCY_CHOICES

class Source(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
