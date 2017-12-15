# -*- coding: utf-8 -*-
import datetime

from django.db import models

import pytz


def handle_unix_timefields(Model, _dict):
    for field in Model._meta.get_fields():
        if isinstance(field, models.DateTimeField):
            _dict[field.name] = datetime.datetime.fromtimestamp(
                int(_dict[field.name]),
            ).replace(tzinfo=pytz.utc)
    return _dict
