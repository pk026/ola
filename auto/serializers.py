# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from auto.models import Trip


class TripSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Trip
        fields = '__all__'