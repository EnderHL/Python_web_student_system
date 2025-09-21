"""
教师应用的视图模块
定义教师管理相关的API视图
"""
from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .models import Teacher
from .serializers import TeacherSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    """教师视图集，提供教师信息的CRUD操作
    
    支持的操作：
    - GET /teachers/：获取教师列表
    - POST /teachers/：创建新教师
    - GET /teachers/{id}/：获取单个教师详情
    - PUT /teachers/{id}/：更新教师信息
    - DELETE /teachers/{id}/：删除教师
    
    权限控制：
    - 开发环境下允许所有用户访问
    - 生产环境将集成JWT认证
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]  # 要求用户必须登录
    
    def create(self, request, *args, **kwargs):
        """创建新教师，处理邮箱唯一性错误并自动关联当前用户
        
        重写create方法，完成以下功能：
        1. 专门捕获邮箱唯一性冲突错误，返回更友好的错误信息
        2. 自动将当前登录用户与新创建的教师资料关联
        """
        try:
            # 自动关联当前登录用户
            request.data['user'] = request.user.id
            return super().create(request, *args, **kwargs)
        except Exception as e:
            if 'email' in str(e).lower() and 'unique' in str(e).lower():
                return Response(
                    {'error': '邮箱已被使用，请使用其他邮箱地址'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            raise
