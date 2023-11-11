from django.shortcuts import render
from .models import Advertise

from .serializers import AdSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from random import randint

class AdAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        count = Advertise.objects.count()
        random_index = randint(0,count-1)
        ad = Advertise.objects.all()[random_index]
        serializer = AdSerializer(ad)
        return Response(serializer.data, status=status.HTTP_200_OK)
