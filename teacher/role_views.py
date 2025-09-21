"""
教师应用的角色视图模块
定义角色管理相关的API视图
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import transaction
from .models import Role, TeacherRole
from .role_serializers import RoleSerializer, TeacherRoleSerializer, TeacherRoleCreateSerializer

class RoleViewSet(viewsets.ModelViewSet):
    """角色视图集，提供角色信息的CRUD操作
    
    支持的操作：
    - GET /roles/：获取角色列表
    - POST /roles/：创建新角色
    - GET /roles/{id}/：获取单个角色详情
    - PUT /roles/{id}/：更新角色信息
    - DELETE /roles/{id}/：删除角色
    
    权限控制：
    - 要求用户必须登录
    - 只有管理员或具有角色管理权限的用户才能操作
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """根据用户权限过滤查询结果"""
        user = self.request.user
        # 管理员可以查看所有角色
        if user.is_admin():
            return Role.objects.all()
        # 教师只能查看自己拥有的角色（通过TeacherRole关联）
        if user.is_teacher():
            # 获取当前教师拥有的角色ID
            teacher_role_ids = TeacherRole.objects.filter(
                teacher=user.teacher_profile
            ).values_list('role_id', flat=True)
            return Role.objects.filter(id__in=teacher_role_ids)
        # 其他用户无权查看角色
        return Role.objects.none()

class TeacherRoleViewSet(viewsets.ModelViewSet):
    """教师角色关联视图集，提供教师与角色关联的管理功能
    
    支持的操作：
    - GET /teacher_roles/：获取教师角色关联列表
    - POST /teacher_roles/：创建教师角色关联
    - GET /teacher_roles/{id}/：获取单个教师角色关联详情
    - DELETE /teacher_roles/{id}/：删除教师角色关联
    - POST /teacher_roles/batch_assign/：批量分配角色给教师
    
    权限控制：
    - 要求用户必须登录
    - 只有管理员或具有角色分配权限的用户才能操作
    """
    queryset = TeacherRole.objects.all()
    serializer_class = TeacherRoleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """根据用户权限过滤查询结果"""
        user = self.request.user
        # 管理员可以查看所有教师角色关联
        if user.is_admin():
            return TeacherRole.objects.all()
        # 教师只能查看自己的角色关联
        if user.is_teacher():
            return TeacherRole.objects.filter(teacher=user.teacher_profile)
        # 其他用户无权查看
        return TeacherRole.objects.none()
    
    @action(detail=False, methods=['post'], serializer_class=TeacherRoleCreateSerializer)
    @transaction.atomic
    def batch_assign(self, request):
        """批量分配角色给多个教师
        
        请求体参数：
        - teacher_ids: 教师ID列表
        - role_ids: 角色ID列表
        
        返回：
        - 成功创建的关联数量
        """
        user = self.request.user
        
        # 只有管理员才能批量分配角色
        if not user.is_admin():
            return Response(
                {'error': '只有管理员才能批量分配角色'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            teacher_ids = serializer.validated_data['teacher_ids']
            role_ids = serializer.validated_data['role_ids']
            
            created_count = 0
            
            # 为每个教师分配每个角色
            for teacher_id in teacher_ids:
                for role_id in role_ids:
                    # 检查关联是否已存在，不存在则创建
                    if not TeacherRole.objects.filter(
                        teacher_id=teacher_id, 
                        role_id=role_id
                    ).exists():
                        TeacherRole.objects.create(
                            teacher_id=teacher_id, 
                            role_id=role_id
                        )
                        created_count += 1
            
            return Response({
                'message': f'成功分配了 {created_count} 个角色关联',
                'created_count': created_count
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)