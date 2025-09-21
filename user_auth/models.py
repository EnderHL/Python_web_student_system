from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    # 用户类型选择
    USER_TYPE_CHOICES = (
        ('admin', '管理员'),
        ('teacher', '教师'),
        ('student', '学生'),
    )
    
    # 添加自定义字段
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='student',
        verbose_name='用户类型'
    )
    
    # 通用字段
    avatar = models.ImageField(
        upload_to='avatars/', 
        null=True, 
        blank=True,
        verbose_name='头像'
    )
    
    phone_number = models.CharField(
        max_length=15, 
        null=True, 
        blank=True,
        verbose_name='手机号码'
    )
    
    bio = models.TextField(
        max_length=500, 
        null=True, 
        blank=True,
        verbose_name='个人简介'
    )
    
    # 自动时间字段
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='创建时间'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='更新时间'
    )
    
    # 关联字段
    # 与教师表关联
    teacher_profile = models.OneToOneField(
        'teacher.Teacher', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='auth_user',
        verbose_name='教师资料'
    )
    
    # 与学生表关联
    student_profile = models.OneToOneField(
        'student.Student', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='user_account',
        verbose_name='学生资料'
    )
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'
        db_table = 'auth_users'
    
    def __str__(self):
        return f'{self.username} ({self.get_user_type_display()})'

    # 辅助方法
    def is_admin(self):
        return self.user_type == 'admin' or self.is_superuser
    
    def is_teacher(self):
        return self.user_type == 'teacher'
    
    def is_student(self):
        return self.user_type == 'student'
