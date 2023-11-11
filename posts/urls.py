from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TreeViewSet

app_name = 'posts'

router = DefaultRouter()
router.register(r'trees', TreeViewSet, basename='tree')

urlpatterns = [
    path('', include(router.urls)),
]
