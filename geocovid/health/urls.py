from django.conf.urls import url
from django.urls import path, include
from .views import DataGeocovidView, ScenarioCovidView


app_name = 'authorize'

urlpatterns = [
    path('covid/', DataGeocovidView.as_view(), name='data-geocovid'),
    path('getScenario/', ScenarioCovidView.as_view(), name='scenario'),
]