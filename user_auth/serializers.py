from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    # 添加额外的密码确认字段
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label='确认密码'
    )
    
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'password', 'password2', 
            'first_name', 'last_name', 'user_type', 
            'phone_number'
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'user_type': {'required': True}
        }
    
    # 验证密码是否匹配
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': '两次输入的密码不匹配'
            })
        
        # 验证邮箱是否已存在
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({
                'email': '该邮箱已被注册'
            })
            
        # 禁止通过注册功能创建管理员账户
        if attrs.get('user_type') == 'admin':
            raise serializers.ValidationError({
                'user_type': '管理员账户不支持注册，请联系系统管理员获取权限'
            })
        
        return attrs
    
    def create(self, validated_data):
        # 创建用户时不包含password2字段
        validated_data.pop('password2')
        
        # 创建用户并设置密码
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type'],
            phone_number=validated_data.get('phone_number', '')
        )
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if not username or not password:
            raise serializers.ValidationError({
                'error': '用户名和密码都是必填项'
            })
        
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    # 获取用户类型的中文显示值
    user_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 
            'user_type', 'user_type_display', 'phone_number', 
            'bio', 'avatar', 'created_at', 'updated_at',
            'is_active', 'is_staff', 'is_superuser'
        )
        read_only_fields = (
            'id', 'username', 'created_at', 'updated_at',
            'is_active', 'is_staff', 'is_superuser'
        )
    
    def get_user_type_display(self, obj):
        # 返回用户类型的中文显示值
        return obj.get_user_type_display()
    
    def update(self, instance, validated_data):
        # 更新用户资料
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        
        # 注意：email字段在这里不允许修改，如需修改需要专门的邮箱修改功能
        # 同样，user_type字段也不允许随意修改
        
        instance.save()
        return instance