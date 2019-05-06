from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.core import serializers

def home(request):
    if request.method == "GET":
        return JsonResponse({"crsf_token": get_token(request)})

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            return JsonResponse({"user": user.id})
        else:
            return JsonResponse({"user": "incorrect credential"})
    else:
        return JsonResponse({"METHOD": "ERROR"})


def end_session(request):
    logout(request)
    return JsonResponse({"you have been logged out": "it has happened"})