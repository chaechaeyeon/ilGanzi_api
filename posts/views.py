#posts/views.py
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User 
from .serializers import TreeSerializer

class TreeWateredView(APIView):
    def post(Self,request,*args,**kwargs):
        user = request.user
        user.totalWatered += 1
        user.watered += 1
        user.save()
        if user.totalWatered >= 80:
            return Response({"message": "max watered"}, status=status.HTTP_400_BAD_REQUEST)
        
        elif user.totalWatered % 20 == 0:
            user.treephase += 1
            user.save()
            return Response({"message": "watering successed"}, status=status.HTTP_200_OK)
        return Response({"message": "watering successed"}, status=status.HTTP_200_OK)  

class TreeResetView(APIView):
    def post(self,request,*args,**kwargs):
        user = request.user

        if user.treephase==5:
            user.treephase=1
            user.totalWatered=0
            user.watered=0
            user.save()

            return Response({'email': user.email}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST) 