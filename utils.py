# -*- coding: utf-8 -*-
import datetime

from django.db import models

import pytz


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
