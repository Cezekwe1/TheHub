from django.shortcuts import render
from django.http import JsonResponse
from utilities.decorators import check
from django.contrib.auth.decorators import login_required
from organizations.models import Membership, OrgInvite, Organization
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import json
# Create your views here.


def orgs(request):
    if not request.user.is_authenticated:
        return JsonResponse({"Error": "You are not logged in"})
    return JsonResponse({"": ""})

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def make_org(request):
    body = json.loads(request.body)
    name = body["name"]
    org = Organization.objects.create(name=name,creator=request.user)
    if org:
        member_set = org.members.all()
        members = []
        for member in member_set:

            members.append({"id": member.id, "username": member.username,"email":member.email})
        return Response({"id":org.id, "name":org.name})
    else:
        return JsonResponse({"error":"invalid parameters"})