from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Post
from .models import Comment

from .serializers import PostSerializer
from .serializers import CommentSerializer


class PostAPIView(APIView):
    ## Define a method to get a object of a class
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        
    def post(self, request):
        request.data['user'] = request.user.id
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, post_id):
        post = self.get_object(post_id) ## to get the specific post 
        request.data['user'] = request.user.id
        serializer = PostSerializer(post, data=request.data) ## update the post with the given data by the auther
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllPostAPIView(APIView):
    permission_classes = [AllowAny]  ## to give permission for all authentication and non-authentication users
    def get(self, request):
        posts = Post.objects.all() ## To get all post 
        post_serializer = PostSerializer(posts, many=True)
        # return the list of post along its comments
        return Response(post_serializer.data, status=status.HTTP_200_OK)




class CommentAPIView(APIView):
    def post(self, request, post_id):
        request.data['user'] = request.user.id
        request.data['post'] = post_id
        print(request.data)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # if serializer is valid then save the comment and return the response below
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) ## return the error 

class PostCommentAPIView(APIView):
    permission_classes = [AllowAny]  ## to give permission for all
    def get(self, request, post_id):
        comments = Comment.objects.filter(post_id=post_id)
        serializer = CommentSerializer(comments, many=True)
        ## return the list of comments of a post
        return Response(serializer.data)
    