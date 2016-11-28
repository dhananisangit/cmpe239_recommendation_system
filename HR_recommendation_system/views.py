from django.shortcuts import render
from django.http import HttpResponse
from .models import postgres
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

def index(request):
    return render(request, "index.html")