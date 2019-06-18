from django.contrib.auth.models import User 
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .serializers import LoginSerializer, UserSerializer, RegisterSerializer
from rest_framework.authtoken.models import Token


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
        friends_set = user.friends_set()
        for org in org_set:
            org_arr.push({id: org.id , members: org.members, creator: org.creator})
        
        if not user.profile.current_organization:
            if org_set:
                org = org_set.last()
                p = user.profile
                p.current_organization =  org
                p.save()
        
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "organizations": org_arr,
            "current_organization": user.profile.current_organization,
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
            "token": token.key 
        })
