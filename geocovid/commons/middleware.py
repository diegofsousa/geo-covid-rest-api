from django.conf import settings
import django
from django.http import HttpResponseBadRequest
import json

from .exceptions import CustomAPIException

if django.VERSION >= (1, 10, 0):
	MIDDLEWARE_MIXIN = django.utils.deprecation.MiddlewareMixin
else:
	MIDDLEWARE_MIXIN = object

class SecurityApplicationKeyMiddleware(MIDDLEWARE_MIXIN):
	def __init__(self, get_response):
		self.get_response = get_response
		
	def process_request(self, request):
		if request.path != '/api/{}/docs'.format(settings.API_VERSION) and request.path != '/api/{}/health-check/'.format(settings.API_VERSION):
			application_key_request = request.headers.get('Applicationkey', None)
			if application_key_request != settings.APPLICATION_KEY:
				return HttpResponseBadRequest(json.dumps({'detail':"A 'ApplicationKey' foi esquecida ou está incorreta."}), content_type='application/json')
		response = self.get_response(request)
		return response