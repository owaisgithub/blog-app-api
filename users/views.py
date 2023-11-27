#from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib import auth
from django.conf import settings

from datetime import datetime
import jwt

from .serializers import RegistrationSerializer
from .serializers import LoginSerializer
from .serializers import LogoutSerializer

import json


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'name' : serializer.data['first_name'] + " " + serializer.data['last_name'],
                'email' : serializer.data['email']
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = auth.authenticate(email=email, password=password)
    
        if user is None:
            return Response({'detail':'invalid credintial'}, status=status.HTTP_401_UNAUTHORIZED)
        
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
        }
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM) # generate a token

        data = {
            'user' : email,
            'token' : token
        }

        return Response(data, status=status.HTTP_200_OK) # return only token
    

class LogoutAPIView(APIView):
    def get(self, request):
        auth_token = request.META.get('HTTP_AUTHORIZATION')
        auth_token = auth_token.split(' ')[1]

        data = {
            'token':auth_token
        }

        # token = BlacklistedToken.objects.create(token=auth_token)
        serializer = LogoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status' : True})
        return Response(serializer.errors)
