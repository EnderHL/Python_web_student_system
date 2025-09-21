"""
教师应用的序列化器模块
定义教师数据的序列化和反序列化规则
"""
from rest_framework import serializers
from .models import Teacher

class TeacherSerializer(serializers.ModelSerializer):
    """教师序列化器，负责教师模型数据的序列化与反序列化
    
    字段说明：
    - id: 教师ID，自动生成
    - user: 关联用户ID
    - username: 关联用户名（如果有）
    - name: 教师姓名
    - age: 教师年龄（18-65岁之间）
    - gender: 教师性别
    - title: 教师职称
    - department: 所属部门
    - email: 邮箱地址（唯一）
    - phone: 联系电话
    - avatar: 头像图片URL
    - hire_date: 入职日期
    - created_at: 创建时间
    - updated_at: 更新时间
    """
    
    # 为user字段提供默认值，确保即使没有关联用户也能正常序列化
    user = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    # 添加用户名字段，方便前端显示
    username = serializers.SerializerMethodField()
    
    def validate_age(self, value):
        """验证教师年龄是否在合理范围内
        
        参数：
        - value: 用户提交的年龄值
        
        返回：
        - 验证通过的年龄值
        
        异常：
        - serializers.ValidationError: 当年龄不在18-65岁范围内时抛出
        """
        if not value:
            raise serializers.ValidationError("年龄不能为空")
        if value < 18 or value > 65:
            raise serializers.ValidationError("教师年龄必须在18-65岁之间")
        return value
    
    def validate_email(self, value):
        """验证邮箱是否已被使用
        
        参数：
        - value: 用户提交的邮箱值
        
        返回：
        - 验证通过的邮箱值
        
        异常：
        - serializers.ValidationError: 当邮箱已被其他教师使用时抛出
        """
        # 检查邮箱是否已存在，排除当前实例
        if self.instance and self.instance.email == value:
            return value
        
        if Teacher.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被其他教师使用")
        return value
        
    def get_username(self, obj):
        """获取关联用户的用户名
        
        参数：
        - obj: Teacher实例对象
        
        返回：
        - 关联用户的用户名（如果有关联用户），否则返回空字符串
        """
        if obj.user:
            return obj.user.username
        return ""
    
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'username', 'name', 'age', 'gender', 'title', 'department', 'email', 
                  'phone', 'avatar', 'hire_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']