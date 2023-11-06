from django.contrib import admin
from django.urls import path

from .views import AuthAPIView, RegisterAPIView, UserAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    path('auth/', AuthAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
]
