from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.models import User
from .models import Post
from .models import Comment
from .models import Like

import pytz


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        utc_timezone = pytz.utc
        ist_timezone =  pytz.timezone('Asia/Kolkata')
        ist_time = value.replace(tzinfo=utc_timezone).astimezone(ist_timezone)

        return ist_time.strftime("%d %b %Y %H:%M:%S")


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentRetrieveSerializer(ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    created_at = CustomDateTimeField()

    class Meta:
        model = Comment
        fields = ['content', 'created_at', 'post', 'user_email']


class LikeCreateSerializer(ModelSerializer):

    def to_representation(self, instance):
        return {"user" : instance["user"][0]}

    class Meta:
        model = Like
        fields = ['post', 'user']



class LikeRetrieveSerializer(ModelSerializer):
    user = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Like
        fields = ['post', 'user']
        # fields = '__all__'


class PostRetrieveSeriaizer(ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    comments = CommentRetrieveSerializer(many=True, read_only=True)
    likes = LikeRetrieveSerializer(many=True, read_only=True)
    updated_at = CustomDateTimeField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'updated_at', 'user_email', 'likes', 'comments']


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'