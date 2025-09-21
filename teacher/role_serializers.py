"""
教师应用的角色序列化器模块
定义角色数据的序列化和反序列化规则
"""
from rest_framework import serializers
from .models import Role, TeacherRole

class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器，负责角色模型数据的序列化与反序列化
    
    字段说明：
    - id: 角色ID，自动生成
    - name: 角色名称
    - description: 角色描述
    - permissions: 权限列表（显示权限名称）
    """
    # 自定义权限字段，只显示权限名称
    permissions = serializers.SerializerMethodField()
    
    def get_permissions(self, obj):
        """获取角色拥有的权限名称列表"""
        return [perm.name for perm in obj.permissions.all()]
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions']
        read_only_fields = ['id']

class TeacherRoleSerializer(serializers.ModelSerializer):
    """教师角色关联序列化器，负责教师与角色关联数据的序列化与反序列化
    
    字段说明：
    - id: 关联ID，自动生成
    - teacher: 教师信息（嵌套显示姓名）
    - role: 角色信息（嵌套显示名称）
    - assigned_at: 分配时间
    """
    # 嵌套显示教师和角色信息
    teacher_name = serializers.ReadOnlyField(source='teacher.name')
    role_name = serializers.ReadOnlyField(source='role.name')
    
    class Meta:
        model = TeacherRole
        fields = ['id', 'teacher', 'teacher_name', 'role', 'role_name', 'assigned_at']
        read_only_fields = ['id', 'assigned_at']

class TeacherRoleCreateSerializer(serializers.ModelSerializer):
    """教师角色关联创建序列化器，用于批量分配角色"""
    # 接受教师ID列表和角色ID列表
    teacher_ids = serializers.ListField(write_only=True)
    role_ids = serializers.ListField(write_only=True)
    
    class Meta:
        model = TeacherRole
        fields = ['teacher_ids', 'role_ids']
        
    def validate(self, attrs):
        """验证教师ID和角色ID是否存在"""
        from .models import Teacher
        from django.contrib.auth.models import Permission
        
        # 验证教师ID是否存在
        for teacher_id in attrs['teacher_ids']:
            if not Teacher.objects.filter(id=teacher_id).exists():
                raise serializers.ValidationError(f'教师ID {teacher_id} 不存在')
        
        # 验证角色ID是否存在
        for role_id in attrs['role_ids']:
            if not Role.objects.filter(id=role_id).exists():
                raise serializers.ValidationError(f'角色ID {role_id} 不存在')
        
        return attrs