from django.shortcuts import render

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer

# 注册视图
class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    
    @transaction.atomic
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # 创建用户
            user = serializer.save()
            
            # 生成JWT令牌
            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            return Response({
                'user': UserProfileSerializer(user).data,
                'tokens': tokens,
                'message': '用户注册成功'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 登录视图
class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            
            # 验证用户凭据
            user = authenticate(username=username, password=password)
            
            if user:
                # 生成JWT令牌
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                
                return Response({
                    'user': UserProfileSerializer(user).data,
                    'tokens': tokens,
                    'message': '登录成功'
                }, status=status.HTTP_200_OK)
            
            return Response(
                {'error': '用户名或密码错误'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 用户资料视图
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # 获取当前登录用户资料
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        # 更新用户资料
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': serializer.data,
                'message': '用户资料更新成功'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 登出视图
class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            # 获取刷新令牌
            refresh_token = request.data.get('refresh')
            if refresh_token:
                # 在当前Simple JWT版本中，我们只验证令牌是否有效，不做黑名单处理
                # 因为配置中已经禁用了黑名单功能（BLACKLIST_AFTER_ROTATION=False）
                try:
                    # 尝试解析令牌以验证其有效性
                    token = RefreshToken(refresh_token)
                    return Response(
                        {'message': '成功登出'},
                        status=status.HTTP_200_OK
                    )
                except Exception:
                    return Response(
                        {'error': '无效的刷新令牌'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            return Response(
                {'error': '缺少刷新令牌'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# 令牌刷新视图（可选，已在urls中使用SimpleJWT的默认视图）
class TokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                access_token = refresh.access_token
                
                return Response({
                    'access': str(access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {'error': '无效的刷新令牌'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(
            {'error': '缺少刷新令牌'}, 
            status=status.HTTP_400_BAD_REQUEST)
