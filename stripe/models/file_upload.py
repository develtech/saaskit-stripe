# -*- coding: utf-8 -*-
# flake8: NOQA: F401
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.fields import json


FILE_UPLOAD_PURPOSE_CHOICES = (
    ('identity document', _('Identity document')),
    ('dispute_evidence', _('Dispute evidence')),
)


class FileUpload(models.Model):
    created = models.DateTimeField()
    purpose = models.CharField(
        max_length=255,
        help_text=(
            'The purpose of the uploaded file. Possible values are '
            '``identity_document``, ``dispute_evidence``.'
        ),
        choices=FILE_UPLOAD_PURPOSE_CHOICES
    )
    size = models.IntegerField(
        help_text=_(
            'The size in bytes of the file upload object.'
        )
    )
    type = models.CharField(
        max_length=255,
        help_text=_(
            'The type of the file returned. Returns one of the following: '
            '``pdf``, ``jpg``, ``png``.'
        )
    )
    url = models.URLField(
        help_text=_(
            'A read-only URL where the uploaded file can be accessed. Will be '
            'nil unless the uploaded file has one of the following purposes: '
            '``dispute_evidence``. Also nil if retrieved with the publishable '
            'API key.'
        )
    )
