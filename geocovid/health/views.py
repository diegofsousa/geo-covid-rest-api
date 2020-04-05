from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from datetime import datetime, timedelta
import re
from .models import CovidPersonalUser
from .serializers import CreateCovidPersonalUserSerializer, UpdateLatitudeLongitudeSerializer, FullResponseCovidPersonalUserSerializer
from .serializers import REGEX_LATITUDE, REGEX_LONGITUDE
from geocovid.commons.exceptions import CustomAPIException
from rest_framework.permissions import IsAuthenticated

class DataGeocovidView(APIView):
	permission_classes = [IsAuthenticated,]
	def get(self, request):
		query = CovidPersonalUser.objects(user=request.user.pk).first()
		if query == None:
			raise CustomAPIException("Nenhum dado relativo à Covid-19 foi encontrado.")
		response_serializer = FullResponseCovidPersonalUserSerializer(query)
		return Response(response_serializer.data)
		
	def post(self, request):
		query = CovidPersonalUser.objects(user=request.user.pk).first()
		serializer = CreateCovidPersonalUserSerializer(data=request.data)
		
		if serializer.is_valid() == False:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			if query == None: serializer.save(user=request.user.pk)
			else: serializer.update(query, request.data)
		return Response(serializer.data)

	def put(self, request):
		query = CovidPersonalUser.objects(user=request.user.pk).first()
		if query == None:
			raise CustomAPIException("Nenhum dado relativo à Covid-19 foi encontrado.")

		serializer = UpdateLatitudeLongitudeSerializer(data=request.data)
		
		if serializer.is_valid() == False:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		else:
			serializer.update(query, request.data)
		
		renew_query = CovidPersonalUser.objects(user=request.user.pk).first()
		response_serializer = FullResponseCovidPersonalUserSerializer(renew_query)
		return Response(response_serializer.data)


class ScenarioCovidView(generics.ListCreateAPIView):
	serializer_class = FullResponseCovidPersonalUserSerializer
	permission_classes = [IsAuthenticated,]

	def get_queryset(self):
		"""
		In this request the user must pass his location to
		get other users close to him. Optional parameters are:
		distance radius, health and limitUpdate status.
		"""
		queryset = CovidPersonalUser.objects.all()
		me_primary_key = CovidPersonalUser.objects.get(user=self.request.user.pk).user
		lat = self.request.GET.get('lat', None)
		lon = self.request.GET.get('lon', None)

		if lat == None or lon == None:
			raise CustomAPIException("Valores 'lat' e/ ou 'lon' não informados")

		if re.search(REGEX_LATITUDE, lat) == None or re.search(REGEX_LONGITUDE, lat) == None:
			raise CustomAPIException("Valores 'lat' e/ ou 'lon' com formatos incorretos")
		
		radius_meters = self.request.GET.get('radius', 1000.0)

		currect_meters_input = False
		
		try:
			meters = float(radius_meters)
			if meters > 0:currect_meters_input = True
		except ValueError:currect_meters_input = False

		if currect_meters_input == False:
			raise CustomAPIException("Valor 'radius' com formato incorreto")

		status = self.request.GET.get('status', None)
		minutes_to_last_update = self.request.GET.get('limitUpdate', 1440)

		currect_minutes_input = False

		try:
			minutes = int(minutes_to_last_update)
			if minutes > 0:currect_minutes_input = True
		except: currect_minutes_input = False

		if currect_minutes_input == False:
			raise CustomAPIException("Valor 'limitUpdate' com formato incorreto")

		datetime_out_minutes = datetime.now() - timedelta(minutes=int(minutes_to_last_update))

		if status == "non_suspect" or status == "suspect" or status == "infected":
			queryset = queryset(coordinates__near=[float(lat), float(lon)], coordinates__min_distance = 0, coordinates__max_distance=float(radius_meters), status=status, last_send_geo__gte=datetime_out_minutes, user__ne=me_primary_key)
		else:
			queryset = queryset(coordinates__near=[float(lat), float(lon)], coordinates__min_distance = 0, coordinates__max_distance=float(radius_meters), last_send_geo__gte=datetime_out_minutes, user__ne=me_primary_key)
		return queryset