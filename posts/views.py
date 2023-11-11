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

    @action(detail=True, methods=['post'], url_path='sefirot_tree')
    def sefirot_tree(self, request, pk=None):
        tree = self.get_object()
        if tree.watered < 1:
            tree.watered += 1
            tree.totalWatered += 1
            tree.save()
           
            if tree.totalWatered == 70:
                if tree.treephase < 5:
                    tree.treephase += 1
                    tree.totalWatered = 0
                tree.save()
            return Response({'물 주기 성공'})
        else:
            return Response({'기본 1일 물 할당량 1번 '})

    @action(detail=True, methods=['post'], url_path='view_ad')
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

            return Response({'광고 후 물 2회차'})

        return Response({'하루치 물 소진 완료'}, status=status.HTTP_400_BAD_REQUEST)