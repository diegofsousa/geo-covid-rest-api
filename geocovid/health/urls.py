from django.conf.urls import url
from django.urls import path, include
from .views import DataGeocovidView


app_name = 'authorize'

urlpatterns = [
    path('covid/', DataGeocovidView.as_view(), name='data-geocovid'),
]