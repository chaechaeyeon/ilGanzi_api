from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TreeResetView,TreeWateredView

app_name = 'posts'



urlpatterns = [
    path('watering/', TreeWateredView.as_view(), name='watering'),
    path('applyTree/', TreeResetView.as_view(), name='applyTree'),
]
