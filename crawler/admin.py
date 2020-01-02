# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import PDF, URL

# Register your models here.
admin.site.register(PDF)
admin.site.register(URL)