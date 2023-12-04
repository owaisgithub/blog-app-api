from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.contrib.auth import authenticate

from .models import User
from .models import BlacklistedToken
from .models import UserImage
from .models import UserDetail
from .models import Follow


class RegistrationSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'handle', 'email', 'password']

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


class UserImageSerializer(ModelSerializer):
    # image = serializers.ImageField(use_url=True)
    class Meta:
        model = UserImage
        fields = ['image', 'user']


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ['dob', 'mobile', 'gender', 'user']


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class FollowersSerializer(ModelSerializer):
    following = serializers.EmailField(source='following.email', read_only=True)
    class Meta:
        model = Follow
        fields = ['following']


class FollowingSerializer(ModelSerializer):
    follower = serializers.EmailField(source='followers.email', read_only=True)
    class Meta:
        model = Follow
        fields = ['follower']


class UserSerializer(ModelSerializer):
    image = serializers.ImageField(source='profile_image.image')
    dob = serializers.DateField(source='user_detail.dob')
    mobile = serializers.CharField(source='user_detail.mobile')
    gender = serializers.CharField(source='user_detail.gender')
    followings = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'handle', 'image', 'dob', 'mobile', 'gender', 'following_count', 'followings', 'follower_count', 'followers']

    def get_followings(self, obj):
        try:
            return self.context['followings']
        except:
            return None

    def get_followers(self, obj):
        try:
            return self.context['followers']
        except:
            return None

    def get_follower_count(self, obj):
        try:
            return self.context['follower_count']
        except:
            return None

    def get_following_count(self, obj):
        try:
            return self.context['following_count']
        except:
            return None
        
        
class UserSearchSerializer(UserSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta(UserSerializer.Meta):
        fields = ['id', 'name', 'image', 'gender', 'following_count', 'followings', 'follower_count', 'followers']
        
    def get_name(self, obj):
        return obj.getFullName()


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'handle']

