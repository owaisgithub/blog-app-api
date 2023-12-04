from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from django.contrib import auth
from django.conf import settings

from datetime import datetime
import jwt
import json

from .serializers import *

from .models import *

from .customMethod import getFollowerAndFollowing

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
            return Response({'detail':'invalid credintials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA
        }
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM) # generate a token

        data = {
            'token' : token,
            'user': user.handle
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
            return Response({'status' : True}, status=status.HTTP_200_OK)
        return Response(serializer.errors)


class ProfileAPIView(APIView):
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            context = getFollowerAndFollowing(request.user.id)
            serializer = UserSerializer(user, context=context)
            return Response(serializer.data)
        except:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error':'user not found'}, status=status.HTTP_404_NOT_FOUND)


class ImageUploadAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        print(request.data)
        serializer = UserImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    def put(self, request):
        print(request.data)
        if not UserDetail.objects.filter(user_id=request.user.id).exists():
            request.data['user'] = request.user.id
            serializer = UserDetailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = UserDetail.objects.get(user_id=request.user.id)
        serializer = UserDetailSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowAPIView(APIView):
    def post(self, request, user_id):
        data = {
            'follower' : request.user.id,
            'following' : user_id
        }
        follow = Follow.getFollow(data)
        if follow:
            follow.delete()
            return Response({'status': 'Unfollow'})
        serializer = FollowSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'Follow'})
        return Response(serializer.errors)


class UserAPIView(APIView):
    def get(self, request, handle):
        try:
            user = User.objects.get(handle=handle)
            context = getFollowerAndFollowing(user.id)
            serializer = UserSearchSerializer(user, context=context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'user': 'not found'}, status=status.HTTP_404_NOT_FOUND)

