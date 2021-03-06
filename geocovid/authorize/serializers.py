from rest_framework import serializers
from rest_framework.serializers import ValidationError as RestFieldValidationError
from rest_framework_mongoengine.serializers import DocumentSerializer
from geocovid.user.models import User
from .models import TemporalyDataUser
from .validators import _regex_validator

class FirstAccessSerializer(DocumentSerializer):
	class Meta:
		model = TemporalyDataUser
		fields = ["name","email"]

	def validate_email(self, value):
		persists_filter_user = User.objects.filter(email=value)
		if persists_filter_user.count() != 0:
			raise RestFieldValidationError("Este email é inválido para cadastro")
		return value

class SecondAccessSerializer(serializers.Serializer):
	password = serializers.CharField(min_length=6, max_length=15, required=True)