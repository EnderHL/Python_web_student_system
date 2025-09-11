"""
学生应用的模型定义
"""
from django.db import models

# Create your models here.
class Student(models.Model):
    """学生模型类，定义学生实体的数据结构"""
    # 学生姓名，最大长度100字符
    name = models.CharField(max_length=100, verbose_name='学生姓名')
    
    # 学生年龄，整数类型
    age = models.IntegerField(verbose_name='学生年龄')
    
    # 学生性别，最大长度100字符
    gender = models.CharField(max_length=100, verbose_name='学生性别')
    
    # 学生专业，最大长度100字符
    major = models.CharField(max_length=100, verbose_name='学生专业')
    
    # 学生邮箱，必须唯一，使用EmailField会自动验证邮箱格式
    email = models.EmailField(unique=True, verbose_name='学生邮箱')

    def __str__(self):
        """返回模型实例的字符串表示，便于在管理后台显示"""
        return self.name
        
    class Meta:
        """模型的元数据配置"""
        verbose_name = '学生'
        verbose_name_plural = '学生管理'