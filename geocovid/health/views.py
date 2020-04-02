from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CovidPersonalUser
from .serializers import CreateCovidPersonalUserSerializer, UpdateLatitudeLongitudeSerializer, FullResponseCovidPersonalUserSerializer
from geocovid.commons.exceptions import CustomAPIException

class DataGeocovidView(APIView):
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