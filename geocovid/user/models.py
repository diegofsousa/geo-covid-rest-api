from django.db import models
from django.core import validators
from django.contrib.auth.models import (
	AbstractBaseUser, UserManager, AbstractUser
)
from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from easy_thumbnails.fields import ThumbnailerImageField
from geocovid.authorize.models import TemporalyDataUser

class User(AbstractUser):

	username = models.CharField(
		'Username',blank=True,max_length=100, null=True, validators=[
			validators.RegexValidator(
				re.compile('^[\w.@+-]+$'),
				'Enter a valid username. '
				'This value must contain only letters, numbers, and '
				'the characters: @/./+/-/_ .'
				, 'invalid'
			)
		],
		help_text='A short name that will be used to uniquely \
		identify you on the platform.'
	)
	name = models.CharField('Name', max_length=100, blank=True)
	last_name = models.CharField('Last name', max_length=100, blank=True, null=True)
	email = models.EmailField('E-mail', unique=True)
	is_staff = models.BooleanField('Staff', default=False)
	is_active = models.BooleanField('Active', default=True)
	date_joined = models.DateTimeField('Date Joined', auto_now_add=True)	
	bio = models.CharField('Bio', max_length=100, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'name']


	class Meta:
		verbose_name = 'User'
		verbose_name_plural = 'Users'

	def first_name(self):
		return self.name.split(" ")[0]
	
	def last_name(self):
		return " ".join(self.name.split(" ")[1:])

	def __str__(self):
		return self.email

@receiver(post_save, sender=User, dispatch_uid="destroy_user_mongo_documents")
def destroy_user_mongo_documents(sender, instance, **kwargs):
	TemporalyDataUser.objects.filter(email=instance.email).delete()