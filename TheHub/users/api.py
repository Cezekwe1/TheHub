from django.contrib.auth.models import User 
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .serializers import LoginSerializer, UserSerializer


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request, *args , **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })


