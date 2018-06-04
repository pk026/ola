# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from auto.models import Trip, Car
from auto.serializers import TripSerializer, TripGetSerializer
from auto.tasks import mark_complete

def home(request):
    return render(request, 'ola/index.html')

def customer_app(request):
    return render(request, 'ola/auto/customer.html')

def driver_app(request):
    return render(request, 'ola/auto/driver_app.html')

def dashboard_app(request):
    return render(request, 'ola/auto/dashboard.html')

class TripViewset(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_serializer_class(self, *args, **kwargs):
        serializer = TripGetSerializer
        if self.request.method in ['POST', 'PATCH']:
            serializer = TripSerializer
        return serializer

    def list(self, request, *args, **kwargs):
        source_app = request.GET.get('source_app')
        user_id = request.GET.get('user_id')
        data = {}
        self.queryset = self.queryset.order_by('-id')
        if source_app=='DRIVER_APP':
            completed_serializer = self.get_serializer(
                self.queryset.filter(
                    driver_id=user_id, status=Trip.COMPLETE
                ), many=True
            )
            ongoing_serializer = self.get_serializer(
                self.queryset.filter(
                    driver_id=user_id, status=Trip.ONGOING
                ), many=True
            )
            waiting_serializer = self.get_serializer(
                self.queryset.filter(
                    status=Trip.WAITING
                ), many=True
            )
            data.update(
                {
                    'completed': completed_serializer.data,
                    'ongoing': ongoing_serializer.data,
                    'waiting': waiting_serializer.data
                }
            )
            return Response(data, status=status.HTTP_200_OK)
        elif source_app=='DASHBOARD_APP':
            return super(TripViewset, self).list(request, *args, **kwargs)
        return Response(
            {'error': 'which platform you are using'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        cars = Car.objects.filter(user_id=user_id, status=Car.AVAILABLE)
        if cars.exists():
            car = cars[0]
            trip = self.get_object()
            if trip.status==Trip.WAITING:
                trip = trip.get_ride(trip.id, user_id, car.id)
                car.status=Car.ON_TRIP
                car.save()
                mark_complete.apply_async((trip.id,), countdown=300)
                serializer = self.get_serializer(trip)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                {'error': 'ride already have taken by some other driver'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'error': 'Have a car registered first'},
            status=status.HTTP_400_BAD_REQUEST
        )