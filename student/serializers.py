from rest_framework import serializers
from .models import Student, Teacher

# 序列化学生，老师列表，以便查询
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'