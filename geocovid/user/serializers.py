from rest_framework import serializers
from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['name', 'email', 'url']

class MeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['name', 'email', 'last_login', 'is_active']

class SimpleUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['name', 'email']

class UserSerializerForRegister(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ["name","email","password"]