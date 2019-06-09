from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.core import serializers
from utilities.decorators import valid_func_method
from django.contrib.auth.models import User
import json

@valid_func_method("GET")
def home(request):
        return JsonResponse({"crsf_token": get_token(request)})

@valid_func_method("POST")
def login(request):
        # if request.session.test_cookie_worked():
        #         print(">>>> TEST COOKIE WORKED!")
        #         request.session.delete_test_cookie()
        # else:
        #         print("cookies aint be sent")
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        print(username,"")
        user = authenticate(request, username=username, password=password)

        if user is not None:
                django_login(request, user)
                return JsonResponse({"user": user.id})
        else:
                return JsonResponse({"user": "incorrect credential"}, status=404)


@valid_func_method("POST")
def signup(request):
        body = json.loads(request.body)
        username = body['username']
        password = body['password']
        email = body['email']
        user = User.objects.create_user(username,email,password)
        if user is not None:
                return JsonResponse({"user": user.id})
        else:
                return JsonResponse({error: "user failed to be created"}, status=404)


def end_session(request):
    

    logout(request)
    
    return JsonResponse({"you have been logged out": "it has happened"})