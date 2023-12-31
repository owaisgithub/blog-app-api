from django.urls import path

from .views import *

urlpatterns = [
    path('post/', PostAPIView.as_view()),
    path('post/<int:post_id>/', PostAPIView.as_view()),  
    path('comment/<int:post_id>/', CommentAPIView.as_view()),
    path('like/<int:post_id>/', LikeAPIView.as_view()),
    path('all-posts/', AllPostAPIView.as_view()),
    path('post-comments/<int:post_id>/', PostCommentAPIView.as_view()),
]