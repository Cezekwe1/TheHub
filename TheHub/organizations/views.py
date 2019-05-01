from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def orgs(request):
    return JsonResponse({"this is it": "boy"})