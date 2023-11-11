#posts/views.py
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User 
from .serializers import TreeSerializer

class TreeViewSet(ModelViewSet):

    serializer_class = TreeSerializer

    def get_queryset(self):
        return User.objects.all()

    @action(detail=True, methods=['get'], url_path='my_tree')
    def my_tree(self, request, pk=None):
        user_tree = self.get_object()
        serializer = TreeSerializer(user_tree)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='watering')
    def watering(self, request):
        user = request.user
        user.totalWatered += 1
        user.watered += 1
        if user.totalWatered >= 80:
            return Response({"message": "max watered"}, status=status.HTTP_400_BAD_REQUEST)
        elif user.totalWatered % 20 == 0:
            user.treephase += 1
        user.save()
        return Response({"message": "watering successed"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='view_ad_watering')
    def view_ad(self, request, pk=None):
        tree = self.get_object()
        if tree.watered == 1:
            tree.totalWatered += 1
            tree.watered += 1
            tree.save()

            if tree.totalWatered == 70:
                if tree.treephase < 5:
                    tree.treephase += 1
                    tree.totalWatered = 0
                tree.save()

            return Response({'AD watering successed'})

        return Response({'하루치 물 소진 완료'}, status=status.HTTP_400_BAD_REQUEST)