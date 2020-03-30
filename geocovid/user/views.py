from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer, MeSerializer
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	permission_classes = [IsAuthenticated,]
	queryset = User.objects.all().order_by('-date_joined')
	serializer_class = UserSerializer

class Me(generics.GenericAPIView):
	"""
	API endpoint that allows users to be viewed or edited.
	"""
	permission_classes = [IsAuthenticated,]
	def get(self, request, format=None):
		"""
		Return a list of all users.
		"""
		print(dir(request.user))
		serializer = MeSerializer(request.user)
		return Response(serializer.data)