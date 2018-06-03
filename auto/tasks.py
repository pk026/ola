# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import pytz
from ola.ola_celery import app

@app.task
def mark_complete(trip_id):
    analytics_app_app_models = __import__(
            'auto.models', fromlist=['Trip']
        )
    Trip = getattr(analytics_app_app_models, 'Trip')
    trip = Trip.objects.get(id=trip_id)
    trip.status=Trip.COMPLETE
    trip.completed_at = datetime.datetime.now().replace(tzinfo=pytz.UTC)
    trip.save()