from .models import User, CodeForFindPw
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            phoneNumber = validated_data['phoneNumber']
        )
        return user
    
class TreeNameSerializer(serializers.Serializer):
    treename = serializers.CharField(max_length=20)

class CodeForFindPwSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeForFindPw
        fields = ['email']