from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import authenticate

from .models import User
from .models import BlacklistedToken


class RegistrationSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(ModelSerializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in..'
            )
        
        if password is None:
            raise serializers.ValidationError(
                'A password is reuired to log in..'
            )
        
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A User is not found.'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'A user is not activated'
            )
        
        return {
            'token':user.token
        }
        # return super().validate(attrs)

class LogoutSerializer(ModelSerializer):
    class Meta:
        model = BlacklistedToken
        fields = '__all__'