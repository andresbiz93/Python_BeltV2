from django.db import models
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z]+[0-9]+|[0-9]+[a-zA-Z]$')

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}

		if 'first_name' in postData:
			if not (len(postData['first_name']) >= 2 and NAME_REGEX.match(postData['first_name'])):
				errors['first_name'] = 'Please enter a valid first name'

		if 'last_name' in postData: 
			if not (len(postData['last_name']) >= 2 and NAME_REGEX.match(postData['last_name'])):
				errors['last_name'] = 'Please enter a valid last name'

		if not (EMAIL_REGEX.match(postData['email'])):
			errors['email'] = 'Please enter a valid email'

		if not (len(postData['password']) >= 8 and PASSWORD_REGEX.match(postData['password'])):
			errors['password'] = 'Please enter a valid password'

		if 'pw_conf' in postData:
			if not (postData['pw_conf'] == postData['password']):
				errors['pw_conf'] = 'Please ensure the password confirmation matches the initial password'

		return errors

class User(models.Model):
	first_name = models.CharField(max_length = 45)
	last_name = models.CharField(max_length = 45)
	email = models.CharField(max_length = 45)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Thought(models.Model):
	content = models.TextField()
	number_likes = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(User, related_name = "messages")
	users_who_like = models.ManyToManyField(User, related_name = "liked_thoughts")
