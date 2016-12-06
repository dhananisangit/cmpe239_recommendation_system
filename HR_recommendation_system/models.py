from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.db import connection
import re, json

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
		rec = []
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM recs WHERE hacker_id=\'%s\'"%s['id'])
			row = cursor.fetchall()
			for i in range(1, len(row[0])):
				challenge_id =  str(row[0][i]).strip()
				cursor.execute("SELECT * FROM challenges WHERE challenge_id=\'%s\'"%challenge_id)
				r = cursor.fetchall()
				rec.append(r)
				i=i+1
			#cursor.execute("DELETE FROM challenges WHERE challenge_id=\'%s\'"%s['challenge_id'])
		return rec

	def successfulSubmission(self, data):
		d =json.dumps(data)
		s = json.loads(d)
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM recs WHERE hacker_id=\'%s\'"%s['id'])
			row = cursor.fetchall()
			cursor.execute("INSERT INTO submission(hacker_id, challenge_id) VALUES(\'%s\', \'%s\') "%(s['hacker_id'],s['challenge_id']))
		return row

	def convertTOFloat(self, data):
		with connection.cursor() as cursor:
			cursor.execute("select s.challenge_id, c.subdomain, s.solved from submissions as s INNER JOIN challenges as c on s.challenge_id=c.challenge_id")
		return row
		
	def insertToFloat(self, data):
		with connection.cursor() as cursor:
			cursor.execute("INSERT INTO final (challenge_id, subdomain, solved) VALUES(\'%f\', \'%f\', \'%f\')"%(final['challenge_id'],final['subdomain'],final['solved']))
			row = cursor.fetchall()
		return row
		
	def Classify(self, data):
		with connection.cursor() as cursor:
			cursor.execute("select distinct hacker_id, sum(solved) AS correct, count(solved) AS total from submissions group by hacker_id,challenge_id order by correct DESC")
			row = cursor.fetchall()
		return row 