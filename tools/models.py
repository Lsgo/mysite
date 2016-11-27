# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from DjangoUeditor.models import UEditorField
from django.core.urlresolvers import reverse

# Create your models here.
@python_2_unicode_compatible
class UpcCode(models.Model):
    ucode = models.CharField(max_length=50)
    upath = models.CharField(max_length=50)
    uflag = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'UPC码'
        verbose_name_plural = 'UPC码'

    def __str__(self):
        return self.ucode
