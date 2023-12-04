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


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentRetrieveSerializer(ModelSerializer):
    comment_user = serializers.EmailField(source='user.handle', read_only=True)
    created_at = CustomDateTimeField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'comment_user']

    


class LikeCreateSerializer(ModelSerializer):

    def to_representation(self, instance):
        return {"user" : instance["user"][0]}

    class Meta:
        model = Like
        fields = ['post', 'user']



class LikeRetrieveSerializer(ModelSerializer):
    like_user = serializers.EmailField(source='user.handle', read_only=True)
    class Meta:
        model = Like
        fields = ['post', 'like_user']
        # fields = '__all__'


class PostRetrieveSeriaizer(ModelSerializer):
    post_user = serializers.EmailField(source='user.handle', read_only=True)
    comments = CommentRetrieveSerializer(many=True, read_only=True)
    # likes = LikeRetrieveSerializer(many=True, read_only=True)
    updated_at = CustomDateTimeField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'updated_at', 'post_user', 'like_count', 'like', 'comments', 'comment_count']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'