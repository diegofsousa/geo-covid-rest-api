from rest_framework import serializers
from rest_framework.serializers import ValidationError as RestFieldValidationError
from rest_framework_mongoengine.serializers import DocumentSerializer
from datetime import datetime
import re
from geocovid.user.models import User
from .models import CovidPersonalUser

REGEX_LATITUDE = '^[+-]?((90\.?0*$)|(([0-8]?[0-9])\.?[0-9]*$))'
REGEX_LONGITUDE = '^[+-]?((180\.?0*$)|(((1[0-7][0-9])|([0-9]{0,2}))\.?[0-9]*$))'

class CreateCovidPersonalUserSerializer(DocumentSerializer):
	class Meta:
		model = CovidPersonalUser
		fields = ["date_birth", "status", "observation"]

	def validate_status(self, value):
		if value == "non_suspect" or value == "suspect" or value == "infected":
			return value
		raise RestFieldValidationError("Os valores válidos para este campo são: 'non_suspect', 'suspect' ou 'infected'.")

	def update(self, instance, validated_data):
		instance.date_birth = validated_data.get('date_birth', instance.date_birth)
		instance.status = validated_data.get('status', instance.status)
		instance.observation = validated_data.get('observation', instance.observation)
		instance.last_update_status = datetime.now()
		instance.save()
		return instance

class FullResponseCovidPersonalUserSerializer(DocumentSerializer):
	class Meta:
		model = CovidPersonalUser
		exclude = ['user','id']

class UpdateLatitudeLongitudeSerializer(serializers.Serializer):
	latitude = serializers.CharField(max_length=200)
	longitude = serializers.CharField(max_length=200)

	def validate_latitude(self, value):
		if re.search(REGEX_LATITUDE, value) == None:
			raise RestFieldValidationError("Valor inválido para este campo.")
		return value

	def validate_longitude(self, value):
		if re.search(REGEX_LONGITUDE, value) == None:
			raise RestFieldValidationError("Valor inválido para este campo.")
		return value

	def update(self, instance, validated_data):
		instance.coordinates = [float(validated_data['latitude']), 
								float(validated_data['longitude'])]
		instance.last_send_geo = datetime.now()
		instance.save()
		return instance