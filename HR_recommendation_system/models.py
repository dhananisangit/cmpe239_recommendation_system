from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db import connection
import re, json
# Create your models here.


class postgres(models.Model):

	def login(self, credentials):
		with connection.cursor() as cursor:
			cursor.execute("SELECT name, id FROM creds WHERE name=\'%s\' "%(credentials['username']))
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

	def getAllRecs(self, id):
		d =json.dumps(id)
		s = json.loads(d)
		print s
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM recs WHERE hacker_id=\'%s\'"%s['id'])
			row = cursor.fetchall()
		return row