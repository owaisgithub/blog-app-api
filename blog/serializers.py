from rest_framework.serializers import ModelSerializer

from users.models import User
from .models import Post
from .models import Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user', 'comments']
        # fields = '__all__'