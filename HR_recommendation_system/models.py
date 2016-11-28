from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db import connection

# Create your models here.


class postgres(models.Model):

	def login(self, credentials):
		with connection.cursor() as cursor:
			cursor.execute("SELECT id FROM credentials WHERE id=\'%s\' AND password=\'%s\'"%(credentials['username'],credentials['password']))
			row = cursor.fetchall()
		return row

	def register(self, credentials):
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO credentials (id, password) VALUES(\'%s\', \'%s\')"%(credentials['username'],credentials['password']))
		return "done"

	def getChallenges(self):
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM challenges")
			row = cursor.fetchall()
		return row