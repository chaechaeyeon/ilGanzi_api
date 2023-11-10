from django.shortcuts import render

import jwt
from rest_framework.views import APIView
from .models import CodeForFindPw
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
from django.core.mail import EmailMessage

from random import *

def resetWatered():
    users = User.objects.all()
    for i in range(users.count()):
        users[i].watered = 1
        users[i].save()
    return

def create_code(): # 보안코드 생성
    code = ''
    for i in range(6):
        if i % 2 == 0:
            c = randint(97,122)
        else:
            c = randint(48,57)
        code += chr(c)
    return code

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
    permission_classes = [AllowAny]
    # id 찾기
    def post(self, request):
        pN = request.data.get('phoneNumber')
        user = get_object_or_404(User, phoneNumber=pN)
        return Response({"email": user.email})
        
class FindPwAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request): # pw 찾기를 위한 보안코드 발송
        serializer = CodeForFindPwSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            pre_instance = CodeForFindPw.objects.filter(email=email)
            if pre_instance: # 보안코드를 계속 발송했을 때 같은 email 객체가 여러개 생길 것을 방지
                pre_instance.delete()
            instance = serializer.save() # email 객체 생성, email 정보만 담겨있음
            code = create_code()
            instance.code = code # 생성된 email 객체에 보안코드 저장
            instance.save()
            subject = "세피로트 비밀번호 보안코드입니다."
            message = "보안코드는 "+ code + " 입니다."
            to = [email]
            if not to[0].endswith('@naver.com'):
                return Response({"message": "not naver mail"}, status=status.HTTP_400_BAD_REQUEST)
            EmailMessage(subject=subject, body=message, to=to).send()
            return Response({"message": "send code success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request): # 보안코드 비교 및 임시토큰 발행
        email = request.data.get("email")
        code = request.data.get("code")
        if email == None or code == None:
            return Response({"message": "no email or code"}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(CodeForFindPw, email=email)
        if code == instance.code:
            user = get_object_or_404(User, email=email)
            token = TokenObtainPairSerializer.get_token(user) # 임시적으로 access 토큰만 발행
            refresh_token = str(token)
            access_token = str(token.access_token)
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist() # refresh_token은 blacklist로 못 쓰게하기
            res = Response(
                {
                    "message": "code is correct",
                    "access": access_token,
                },
                status=status.HTTP_200_OK,
            )
            instance.delete() # 보안코드를 올바르게 작성했을 경우 email 객체 삭제
            return res
        return Response({"message": "wrong code"}, status=status.HTTP_400_BAD_REQUEST)

class PwResetAPIView(APIView):
    def post(self, request): # pw 변경
        user = request.user
        password = request.data["password"]
        user.set_password(password)
        user.save()
        return Response({"message": "password changed."}, status=status.HTTP_202_ACCEPTED)