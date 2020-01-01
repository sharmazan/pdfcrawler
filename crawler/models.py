# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class PDF(models.Model):
    filename = models.CharField(max_length=255)

    def __unicode__(self):
        return self.filename


class URL(models.Model):
    uri = models.URLField()
    pdfs = models.ManyToManyField(PDF, related_name='urls')
    alive = models.BooleanField()

    def __unicode__(self):
        return self.uri