# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Car(models.Model):
    ON_TRIP = ''
    AVAILABLE = ''
    OFF_DUTY = ''
    STATUS_OPTIONS = (
        (ON_TRIP, 'on_trip'),
        (AVAILABLE, 'available'),
        (OFF_DUTY, 'off_duty'),
    )
    user = models.ForeignKey(User)
    rto_no = models.CharField(max_length=32)
    status = models.CharField(max_length=16, choices=STATUS_OPTIONS)
    model_info = models.CharField(max_length=64, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Trip(models.Model):
    WAITING =  'waiting'
    ONGOING = 'ongoing'
    COMPLETE = 'complete'
    STATUS_OPTIONS = (
        (WAITING, 'waiting'),
        (ONGOING, 'ongoing'),
        (COMPLETE, 'complete'),
    )
    user = models.ForeignKey(User)
    driver = models.ForeignKey(
        User, related_name='trips_drived', null=True, blank=True
    )
    car = models.ForeignKey(Car, null=True, blank=True)
    source = models.CharField(max_length=64, null=True, blank=True)
    destination = models.CharField(max_length=64, null=True, blank=True)
    status = models.CharField(
        max_length=8, default=WAITING, choices=STATUS_OPTIONS, db_index=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)