from django.shortcuts import render

import jwt
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
# from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, get_object_or_404
# from config.settings import SECRET_KEY

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    # 회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                    "treeimage": "static/treephase/treephase{0}.png".format(user.treephase),
                },
                status=status.HTTP_200_OK,
            )
            
            # jwt 토큰 => 쿠키에 저장
            # res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    # 회원 정보 조회
    def get(self, request):
        try:
            user = request.user
            serializer = UserSerializer(instance=user)
            queryset = User.objects.filter(is_staff=False)
            totalUser = queryset.count()
            return Response({
                    "user": serializer.data,
                    "treeimage": "static/treephase/treephase{0}.png".format(user.treephase),
                    "totalUser": totalUser,
                },
                status=status.HTTP_200_OK,)

        except(AttributeError):
            return Response({"message": "no token"}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        # user = request.user
        user = get_object_or_404(User, id=request.user.id)
        serializer = TreeNameSerializer(data=request.data)
        if serializer.is_valid():
            treename = serializer.data.get('treename')
            user.treename = treename
            user.save()
            return Response({"message": "tree name changed"}, status=status.HTTP_200_OK,)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AuthAPIView(APIView):
    permission_classes = [AllowAny]
        
    # 로그인
    def post(self, request):
        # 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이메일, 비번이 맞았을 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            update_last_login(None, user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                    "treeimage": "static/treephase/treephase{0}.png".format(user.treephase),
                },
                status=status.HTTP_200_OK,
            )

            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        else: # 이메일이나 비번 둘 중 하나가 틀렸을 때
            return Response({"message": "Login failed"}, status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        data = {'refresh': request.COOKIES.get('refresh', None)}
        if data['refresh'] == None:
            return Response({"message": "Not login state"}, status=status.HTTP_400_BAD_REQUEST)
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        token = RefreshToken(data['refresh'])
        token.blacklist()
        response.delete_cookie("refresh")
        return response
    
class FindIdAPIView(APIView):
    # id 찾기
    permission_classes = [AllowAny]
    def post(self, request):
        pN = request.data.get('phoneNumber')
        user = get_object_or_404(User, phoneNumber=pN)
        return Response({"email": user.email})
        
class FindPwAPIView(APIView):
    # pw 찾기
    def post(self, request):
        pass
