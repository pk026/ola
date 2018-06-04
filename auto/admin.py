# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from auto.models import Car, Trip

admin.site.register(Car)
admin.site.register(Trip)