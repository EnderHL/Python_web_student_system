"""
学生应用的序列化器定义
"""
from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    """
    学生序列化器，用于学生数据的序列化和反序列化
    - 序列化：将模型实例转换为JSON格式
    - 反序列化：将JSON数据转换为模型实例并进行验证
    """
    class Meta:
        # 指定使用的模型类
        model = Student
        # 指定序列化的字段列表
        fields = ['id', 'name', 'age', 'gender', 'major', 'email']
        # 指定只读字段（不会被反序列化更新）
        read_only_fields = ['id']

    def validate_age(self, value):
        """
        验证年龄字段的有效性
        - 确保年龄不为空
        - 确保年龄在合理范围内（0-100岁）
        """
        if value is None:
            raise serializers.ValidationError('age is required')
        if value < 0 or value > 100:
            raise serializers.ValidationError('age must be between 0 and 100')
        return value

    def validate_email(self, value):
        """
        验证邮箱字段的有效性
        - 确保邮箱地址的唯一性
        - 在更新操作时排除当前实例
        """
        qs = Student.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A student with this Email already exists.')
        return value





