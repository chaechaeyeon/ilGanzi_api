#posts/serializers.py
from rest_framework import serializers
from accounts.models import User

class TreeSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='email', read_only=True)
    user_treename = serializers.CharField(source='treename', read_only=True)
    class Meta:
        model = User
        fields=['id','user_email','user_treename','treephase','totalWatered','watered']