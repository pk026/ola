# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import pytz
from django.db import models
from django.db import transaction
from django.contrib.auth.models import User

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
    status = models.CharField(
        max_length=16, default=AVAILABLE, choices=STATUS_OPTIONS
    )
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
    completed_at = models.DateTimeField(null=True, blank=True)
    pickup_at = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_ride(cls, trip_id, driver_id, car_id):
        with transaction.atomic():
            trip = (
                cls.objects
                .select_for_update()
                .get(id=trip_id)
            )
            trip.driver_id=driver_id
            trip.car_id=car_id
            trip.status=cls.ONGOING
            trip.pickup_at=datetime.datetime.now().replace(tzinfo=pytz.UTC)
            trip.save()
        return trip
