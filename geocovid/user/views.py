from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from .models import User
from .serializers import UserSerializer, MeSerializer
from rest_framework.response import Response

me_response = openapi.Response('Modelo de resposta', MeSerializer)
@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_description="Retorna os dados do usuário que está logado.",
	responses={200: me_response}
))
class Me(generics.GenericAPIView):
	"""
	Returns the logged user data.
	"""
	permission_classes = [IsAuthenticated,]
	def get(self, request, format=None):
		serializer = MeSerializer(request.user)
		return Response(serializer.data)