"""ola URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers
from auto.views import TripViewset
from auto.views import home, customer_app, driver_app, dashboard_app

router = routers.DefaultRouter()
router.register(r'api/v1/trip', TripViewset, base_name='event')
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^customer/$', customer_app, name='customer'),
    url(r'^dashboard/$', dashboard_app, name='dashboard'),
    url(r'^driver_app/$', driver_app, name='driver_app'),
]
urlpatterns += router.urls