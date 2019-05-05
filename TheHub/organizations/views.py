from django.shortcuts import render
from django.http import JsonResponse
from utilities.decorators import check
from utilities.secrets import THEKEY
# Create your views here.

def orgs(request):
    return JsonResponse({"this is it": "cripppp"})
    