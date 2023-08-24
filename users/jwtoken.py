from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.conf import settings

import jwt

from .models import User
from .models import BlacklistedToken


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # print(request.META.get('HTTP_AUTHORIZATION'))
        token = self.get_token_from_request(request)
        if token is None:
            return None
        
        if self.is_token_blacklisted(token):
            # print("token is blacklist")
            raise AuthenticationFailed('Token is invalid')

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]) ## decode the token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token is invalid')

        user_id = payload.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
        

        return (user, None)
    
    def is_token_blacklisted(self, token):
        if BlacklistedToken.objects.filter(token=token).exists():
            return True
        return False

    def get_token_from_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None
