from django.urls import path

from .views import *

urlpatterns = [
    path('create/', RegistrationAPIView.as_view()),
    path('authenticate/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
]