from django.shortcuts import render
from django.http import JsonResponse
from utilities.decorators import check
from utilities.secrets import THEKEY
from django.contrib.auth.decorators import login_required
# Create your views here.


def orgs(request):
    if not request.user.is_authenticated:
        return JsonResponse({"Error": "You are not logged in"})
    return JsonResponse({"this is it": "cripppp"})
    