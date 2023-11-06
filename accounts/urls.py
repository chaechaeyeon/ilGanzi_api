from django.contrib import admin
from django.urls import path

from .views import AuthAPIView, RegisterAPIView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'accounts'

urlpatterns = [
    path('auth/', AuthAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
]
