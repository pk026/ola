# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from auto.models import Trip
from auto.serializers import TripSerializer


class TripViewset(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def list(self, request, *args, **kwargs):
        pass