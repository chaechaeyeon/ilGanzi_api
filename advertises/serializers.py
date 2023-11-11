from .models import Advertise
from rest_framework import serializers

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertise
        fields = '__all__'