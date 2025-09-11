"""
学生应用的视图定义
"""
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.db import IntegrityError, transaction
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import Student
from .serializers import StudentSerializer

class StudentViewSet(ModelViewSet):
    """
    学生视图集，提供完整的学生管理CRUD操作
    - GET /api/students/ - 获取学生列表
    - POST /api/students/ - 创建新学生
    - GET /api/students/{id}/ - 获取单个学生详情
    - PUT /api/students/{id}/ - 更新学生信息
    - DELETE /api/students/{id}/ - 删除学生
    """
    # 查询集：获取所有学生数据
    queryset = Student.objects.all()
    
    # 序列化器：用于数据的序列化和反序列化
    serializer_class = StudentSerializer
    
    # 权限控制：允许任何用户进行任何操作（适合开发环境）
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        重写create方法，添加数据库事务和唯一性错误处理
        确保在邮箱重复时返回友好的错误信息
        """
        # 获取序列化器并验证数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # 使用事务确保数据一致性
            with transaction.atomic():
                self.perform_create(serializer)
        except IntegrityError:
            # 捕获并处理邮箱唯一性冲突
            return Response(
                {"email": ["已存在一个同邮箱的学生"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 获取成功响应头并返回创建的数据
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



