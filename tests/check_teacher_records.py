#!/usr/bin/env python
"""
检查数据库中的教师记录
确保能直接运行并正确加载Django设置
"""
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')

# 导入Django并初始化
import django
django.setup()

# 导入模型并查询数据
from teacher.models import Teacher

print('数据库中教师记录数量:', Teacher.objects.count())
print('\n教师记录详情:')
for teacher in Teacher.objects.all():
    print(f'ID: {teacher.id}, 姓名: {teacher.name}, 用户ID: {teacher.user_id}')