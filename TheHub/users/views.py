from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.core import serializers
from utilities.decorators import valid_func_method
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from organizations.models import Membership, OrgInvite, Organization
from users.models import Invite, Friends
from rest_framework import status
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

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def end_session(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def search(request,query_str):
        user_arr = []
        users = []
        users = User.objects.filter( username__startswith=query_str)


        if users:
                for u in users:
                        user_arr.append({"id": u.id, "username": u.username, "email": u.email})
        return Response({"users": user_arr})

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_person(request,user_id):
        u = User.objects.filter(id=user_id)
        if u:
                u = u[0]
        else:
                return JsonResponse({"error": "user not found"}, status=404)
        
        is_friend = False
        is_org_member = False
        is_admin = False
        friends_set = u.profile.friends.all()
        org_set = u.organization_set.all()
        org_arr = []
        user_current_org = request.user.profile.get_current_org()
        membership = Membership.objects.filter(user=u,organization=user_current_org)
        pending_org_invite_set = OrgInvite.objects.filter(target=u,organization=user_current_org, accepted=None)
        pending_friend_invite_set = Invite.objects.filter(target=u,inviter=request.user, accepted=None)
        pending_org_invite = False
        pending_friend_invite = False
        if pending_org_invite_set: 
                pending_org_invite = True
        
        if pending_friend_invite_set:
                pending_friend_invite = True 
                


        if membership:
                is_org_member = True
                membership = membership[0]
                is_admin = membership.administrator

        if friends_set:
                print(friends_set)
                for friend in friends_set:
                        if (friend.id == request.user.profile.id):
                                is_friend = True
                                break;
        
        if org_set:
                for org in org_set:
                        org_arr.append({"id": org.id, "name": org.name})

        return Response({"user": 
                        {"id": u.id, 
                        "username": u.username,
                        "email": u.email, 
                        "organizations": org_arr,
                        "are_friends": is_friend,
                        "is_member": is_org_member,
                        "is_admin":is_admin,
                        "pending_org":pending_org_invite,
                        "pending_friend":pending_friend_invite
                        }})
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def send_invite(request,invite_type):
        if invite_type == "friend":
                body = json.loads(request.body)
                u = User.objects.filter(id=body["target_id"])
                if u:
                        u = u[0]
                        i = Invite.objects.create(inviter=request.user,target=u)
                        if i:
                                return Response({"obj": {"id": i.id}})
                        else:
                                return JsonResponse({"invalid":"invite cant be created"},status=404)
        elif invite_type == "org":
                body = json.loads(request.body)
                u = User.objects.filter(id=body["target_id"])
                if u:
                        u = u[0]
                        p = request.user.profile.get_current_org()
                        if p:
                                i = OrgInvite.objects.create(inviter=request.user,organization=p,target=u)
                                if i:
                                        return Response({"obj": {"id": i.id}})
                                else:
                                        return JsonResponse({"invalid":"invite cant be created"},status=404)
                        else:
                                return JsonResponse({"invalid":"No profile"},status=404)
                else:
                        return JsonResponse({"invalid":"no user"},status=404)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def remove_person(request,removal_type):
        if removal_type == "friend":
                body = json.loads(request.body)
                friend_set = request.user.profile.friends.all()
                del_friend = None
                fried_trial = Friends.objects.filter(inviter=request.user.profile)
                fried_two = Friends.objects.filter(target=request.user.profile)
                for friend in friend_set:
                        print(friend.user.id,body["target_id"])
                        if friend.user.id == body["target_id"]:
                                friend.friends.remove(request.user.profile)
                                request.user.profile.friends.remove(friend)
                                del_friend = friend
                                break;
                if del_friend:
                        
                        return Response({"del_user":{"id": del_friend.user.id, "username": del_friend.user.username, "email": del_friend.user.email}})
                else:
                        return JsonResponse({"error":"invalid"},status=404)
        elif removal_type == "org":
                body = json.loads(request.body)
                print(body["target_id"])

                m = Membership.objects.filter(user=body["target_id"], organization=body["organization"])
                if m:
                        m = m[0]
                        m.delete()
                        return Response({"member":{"organization_id":m.organization.id, "organization_name":m.organization.name}})
                else: 
                        return JsonResponse({"error":"invalid"},status=404)

@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def make_admin(request):
        body = json.loads(request.body)
        m = Membership.objects.filter(organization=body["organization_id"], user=body['target_id'])
        if m:
                m = m[0]
                m.administrator = True
                m.save()
                return Response({"id": m.id, "organization":{"id": m.organization.id , "name": m.organization.name}, "administrator": m.administrator})
        else:
                return JsonResponse({"error":"invalid"},status=404 )


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def change_current_org(request):
        org_set = request.user.organization_set.all()
        body = json.loads(request.body)
        org_id = body["org_id"]
        

        for org in org_set:
                if org.id == org_id:
                        request.user.profile.current_organization = org
                        request.user.profile.save()
                        print(request.user.profile.current_organization)
                        is_creator = org.creator.id == request.user.id
                        is_admin = Membership.objects.get(user=request.user.id, organization=org.id).administrator
                        org_members = []
                        member_set = org.members.all()
                        for member in member_set:
                                org_members.append({"id": member.id , "username": member.username, "email": member.email})
                        return Response({"current_organization":{"id":org.id, "name":org.name, "is_creator":is_creator, "is_admin":is_admin}, "members":org_members})
                        
        return JsonResponse({"error": "invalid"}, status=404)

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_notifications(request):
        org_invites = OrgInvite.objects.filter(target=request.user, accepted=None)
        friend_requests = Invite.objects.filter(target=request.user, accepted=None)
        accepted_org_invites = OrgInvite.objects.filter(inviter=request.user, accepted=True)
        accepted_friend_requests = Invite.objects.filter(inviter=request.user, accepted=True)

        org_invites_arr = []
        friend_request_arr = []
        accepted_invites_arr = []
        accepted_requests_arr = []

        if org_invites:
                for invite in org_invites:
                        org_invites_arr.append({"id": invite.id, "inviter": {"id": invite.inviter.id, "username":invite.inviter.username, "email":invite.inviter.email}, "target": {"id": invite.target.id, "username":invite.target.username, "email":invite.target.email}, "organization":{"id":invite.organization.id, "name":invite.organization.name}})
        
        if friend_requests:
                for invite in friend_requests:
                        friend_request_arr.append({"id": invite.id, "inviter":{"id": invite.inviter.id, "username":invite.inviter.username, "email":invite.inviter.email}, "target":{"id": invite.target.id, "username":invite.target.username, "email":invite.target.email}})
        
        if accepted_org_invites:
                for accepted_invites in accepted_org_invites:
                        accepted_invites_arr.append({"id":accepted_invites.id, "inviter":{"id": accepted_invites.inviter.id, "username":accepted_invites.inviter.username, "email":accepted_invites.inviter.email},"target": {"id": accepted_invites.target.id, "username":accepted_invites.target.username, "email": accepted_invites.target.email}, "organization":{"id":accepted_invites.organization.id, "name":accepted_invites.organization.name}})
        
        if accepted_friend_requests:
                for accepted_invites in accepted_friend_requests:
                        accepted_requests_arr.append({"id":accepted_invites.id, "inviter":{"id": accepted_invites.inviter.id, "username":accepted_invites.inviter.username, "email":accepted_invites.inviter.email},"target": {"id": accepted_invites.target.id, "username":accepted_invites.target.username, "email": accepted_invites.target.email}})
        
        return Response({"org_invites":org_invites_arr, "friend_requests":friend_request_arr, "accepted_org_invites":accepted_invites_arr, "accepted_friend_requests":accepted_requests_arr})
        
@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def answer_invite(request,type):
        if type == "org":
                body = json.loads(request.body)
                id = body["id"]
                val = body["accepted"]
                invite = OrgInvite.objects.filter(id=id)
                if invite:
                        invite = invite[0]
                        invite.accepted = val
                        invite.save()
                        current_org_obj = {}
                        current_organization = request.user.profile.get_current_org()
                        organization_members = []
                        if val:
                                if current_organization:
                                        members_set = current_organization.members.all()
                                        for member in members_set:
                                                organization_members.append({"id": member.id, "username": member.username, "email": member.email})
                                        current_org_obj = {"id": current_organization.id , "name": current_organization.name}
                                return Response({"meta_data": {"id": invite.id, "type":"org"} , "new_org": {"id": invite.organization.id, "name": invite.organization.name}, "current_organization": current_org_obj, "organzation_members": organization_members})
                        else:
                                return Response({"meta_data": {"id": invite.id, "type":"org"}, "new_org": false, "current_organization": false, "organization_members": []})

                else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
        elif type == "friend":
                body = json.loads(request.body)
                id = body["id"]
                val = body["accepted"]
                invite = Invite.objects.filter(id=id)
                if invite:
                        invite = invite[0]
                        invite.accepted = val
                        invite.save()
                        if val:
                                return Response({"meta_data":{"id": invite.id, "type":"friend"}, "new_friend": {"id": invite.inviter.id, "username": invite.inviter.username, "email": invite.inviter.email }})
                        else:
                                return Response({{"meta_data":{"id": invite.id, "type":"friend"}, "new_friend": false}})
                else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def remove_invites(request):
        
        body = json.loads(request.body)
        org_invites = body["accepted_org_invites"]
        
        for invite in org_invites:
                o = OrgInvite.objects.filter(id=invite["id"])
                if o:
                        o = o[0]
                        o.delete()

        friend_requests = body["accepted_friend_requests"]
        print(friend_requests)
        for invite in friend_requests:
                i = Invite.objects.filter(id=invite["id"])
                if i:
                        i = i[0]
                        i.delete()
        return Response(status=status.HTTP_200_OK)

        
                


        




