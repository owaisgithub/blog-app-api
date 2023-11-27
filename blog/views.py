from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from django.db.models import Q

from .models import Post
from .models import Comment
from .models import Like

from .serializers import PostRetrieveSeriaizer
from .serializers import PostCreateSerializer
from .serializers import CommentCreateSerializer
from .serializers import CommentRetrieveSerializer
from .serializers import LikeCreateSerializer
from .serializers import LikeRetrieveSerializer


class PostAPIView(APIView):
    ## Define a method to get a object of a class
    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def getCommentsByPostId(self, post_id):
        try:
            return Comment.objects.filter(post_id = post_id)
        except Comment.DoesNotExist:
            return status.HTTP_404_NOT_FOUND

    ## Get all post of login user.
    def get(self, request):
        user_id = request.user.id
        posts = Post.objects.filter(user_id=user_id)
        # print(posts[1].formateDatetime)
        serializer = PostRetrieveSeriaizer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    ## Post by the login user
    def post(self, request):
        request.data['user'] = request.user.id
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, post_id):
        post = self.get_post(post_id) ## to get the specific post 
        request.data['user'] = request.user.id
        serializer = PostCreateSerializer(post, data=request.data) ## update the post with the given data by the auther
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = self.get_post(post_id)
        # comments = self.getCommentsByPostId(post.id)
        comments = post.comments.all()
        comments.delete()
        post.delete()
        return Response({'status' : True}, status=status.HTTP_200_OK)


class AllPostAPIView(APIView):
    permission_classes = [AllowAny]  ## to give permission for all authentication and non-authentication users
    def get(self, request):
        posts = Post.objects.all() ## To get all post 
        post_serializer = PostSerializer(posts, many=True)
        # return the list of post along its comments
        return Response(post_serializer.data, status=status.HTTP_200_OK)


class CommentAPIView(APIView):
    ##Leave The comments
    def post(self, request, post_id):
        request.data['user'] = request.user.id
        request.data['post'] = post_id
        print(request.data)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # if serializer is valid then save the comment and return the response below
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) ## return the error 

class PostCommentAPIView(APIView):
    permission_classes = [AllowAny]  ## to give permission for all
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentCreateSerializer(comments, many=True)
        ## return the list of comments of a post
        return Response(serializer.data)


class LikeAPIView(APIView):
    def post(self, request, post_id):
        print(request.user.id)
        data = {
            'user' : request.user.id,
            'post' : post_id
        }
        like = Like.objects.filter(Q(post_id=post_id) & Q(user_id=data['user']))
        if like:
            like.delete()
            return Response({'msg' : 'dislike'}, status=status.HTTP_200_OK)

        serializer = LikeCreateSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg' : 'liked'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)