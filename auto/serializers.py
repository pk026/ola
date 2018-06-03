# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import pytz
from rest_framework import serializers
from auto.models import Trip


class TripSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Trip
        fields = '__all__'
    
class TripGetSerializer(serializers.ModelSerializer):
    request_time_lapsed = serializers.SerializerMethodField()
    pickup_time_lapsed = serializers.SerializerMethodField()
    completed_time_lapsed = serializers.SerializerMethodField()

    def get_request_time_lapsed(self, obj):
        return datetime.datetime.now().replace(tzinfo=pytz.UTC) - obj.created

    def get_pickup_time_lapsed(self, obj):
        if obj.status in [Trip.ONGOING, Trip.COMPLETE]:
            return datetime.datetime.now().replace(tzinfo=pytz.UTC) - obj.pickup_at
        return None

    def get_completed_time_lapsed(self, obj):
        if obj.status==Trip.COMPLETE:
            return datetime.datetime.now().replace(tzinfo=pytz.UTC) - obj.completed_at
        return None

    class Meta(object):
        model = Trip
        fields = '__all__'