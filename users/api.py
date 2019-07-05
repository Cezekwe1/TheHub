from django.contrib.auth.models import User 
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .serializers import LoginSerializer, UserSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token
from organizations.models import Membership


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args , **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = Token.objects.get_or_create(user=user)
        org_arr = []
        org_set = user.organization_set.all()
        friends = []
        friends_set = user.profile.friends.all()
        members_arr = []
        current_org = user.profile.get_current_org()
        current_org_object = {}

        if current_org:
            members_set = current_org.members.all()
            is_creator = True if current_org.creator.id == user.id else False
            is_admin = Membership.objects.get(user=user.id, organization=current_org.id).administrator
            current_org_object = {"id": current_org.id, "name": current_org.name, "is_creator": is_creator, "is_admin": is_admin}

            for member in members_set:
                obj = {"id": member.id , "username": member.username}
                members_arr.append(obj)
        
        for friend in friends_set:
            obj = {"id": friend.user.id, "username": friend.user.username}
            friends.append(obj)

        for org in org_set:
            org_arr.append({"id": org.id, "name": org.name})
        
        
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "organizations": org_arr,
            "current_organization": current_org_object,
            "friends": friends,
            "organization_members": members_arr,
            "token": token[0].key
        })


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer


    def post(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "organizations": [],
            "current_organization": None,
            "friends": [],
            "organization_members": [],
            "token": token.key  
        })
