from django.urls import path

from .views import *

urlpatterns = [
    path('create/', RegistrationAPIView.as_view()),
    path('authenticate/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('upload/', ImageUploadAPIView.as_view()),
    path('user-detail/', UserDetailAPIView.as_view()),
    path('follow/<int:user_id>/', FollowAPIView.as_view()),
    path('<handle>/', UserAPIView.as_view()),
]