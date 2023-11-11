from django.contrib import admin
from django.urls import path

from .views import AdAPIView

app_name = 'advertises'

urlpatterns = [
    path('advertise/', AdAPIView.as_view()),
]
