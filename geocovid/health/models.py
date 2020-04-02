from django.db import models
from mongoengine import Document, EmbeddedDocument, fields
from datetime import datetime
from uuid import uuid4
from geocovid.user.models import User


class CovidPersonalUser(Document):

	user = fields.LongField(required=True)
	date_birth = fields.DateField(required=True)
	last_send_geo = fields.DateTimeField()
	last_update_status = fields.DateTimeField(default=datetime.now)
	created_at = fields.DateTimeField(default=datetime.now)
	status = fields.StringField(required=True)
	observation = fields.StringField()
	latitude = fields.StringField()
	longitude = fields.StringField()

	class Meta:
		verbose_name = 'CovidPersonalUser'
		verbose_name_plural = 'CovidPersonalUsers'

	def __str__(self):
		return User.objects.get(pk=self.user).name
