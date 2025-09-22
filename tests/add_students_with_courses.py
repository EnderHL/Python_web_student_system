#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
添加学生记录并为这些学生关联课程信息的脚本

功能：
1. 添加若干学生记录到数据库
2. 为这些学生关联相应的课程信息
3. 输出操作结果
"""
import os
import sys
import django
import random
from datetime import datetime, timedelta

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')
django.setup()

# 导入模型
from student.models import Student
from course.models import Course, Enrollment
from teacher.models import Teacher

# 示例数据
STUDENTS = [
    {
        'name': '张三',
        'age': 20,
        'gender': '男',
        'class_name': '计算机1班',
        'student_id': '20220011',
        'college': '信息学院',
        'major': '计算机科学与技术',
        'email': 'zhangsan_new@example.com',
        'phone': '13800138011'
    },
    {
        'name': '李四',
        'age': 21,
        'gender': '女',
        'class_name': '计算机2班',
        'student_id': '20220012',
        'college': '信息学院',
        'major': '软件工程',
        'email': 'lisi_new@example.com',
        'phone': '13800138012'
    },
    {
        'name': '王五',
        'age': 20,
        'gender': '男',
        'class_name': '计算机1班',
        'student_id': '20220013',
        'college': '信息学院',
        'major': '人工智能',
        'email': 'wangwu_new@example.com',
        'phone': '13800138013'
    },
    {
        'name': '赵六',
        'age': 22,
        'gender': '女',
        'class_name': '计算机2班',
        'student_id': '20220014',
        'college': '信息学院',
        'major': '数据科学',
        'email': 'zhaoliu_new@example.com',
        'phone': '13800138014'
    },
    {
        'name': '钱七',
        'age': 21,
        'gender': '男',
        'class_name': '计算机1班',
        'student_id': '20220015',
        'college': '信息学院',
        'major': '网络工程',
        'email': 'qianqi_new@example.com',
        'phone': '13800138015'
    }
]

# 示例课程数据
COURSES = [
    {
        'name': '数据结构',
        'code': 'CS001',
        'credits': 4.0,
        'description': '介绍数据结构的基本概念和算法',
        'total_hours': 64,
        'semester': '2024-春季'
    },
    {
        'name': '操作系统',
        'code': 'CS002',
        'credits': 4.0,
        'description': '介绍操作系统的基本原理和实现',
        'total_hours': 64,
        'semester': '2024-春季'
    },
    {
        'name': '计算机网络',
        'code': 'CS003',
        'credits': 3.0,
        'description': '介绍计算机网络的基本概念和协议',
        'total_hours': 48,
        'semester': '2024-春季'
    },
    {
        'name': '数据库原理',
        'code': 'CS004',
        'credits': 4.0,
        'description': '介绍数据库系统的基本原理和设计',
        'total_hours': 64,
        'semester': '2024-春季'
    },
    {
        'name': '软件工程',
        'code': 'CS005',
        'credits': 3.0,
        'description': '介绍软件工程的基本概念和方法',
        'total_hours': 48,
        'semester': '2024-春季'
    }
]


def add_courses_if_not_exists():
    """添加课程数据（如果不存在）"""
    print("\n=== 添加课程数据 ===")
    course_objects = []
    
    for course_data in COURSES:
        course, created = Course.objects.get_or_create(
            code=course_data['code'],
            defaults=course_data
        )
        if created:
            print(f"✓ 创建课程: {course.name} (代码: {course.code})")
        else:
            print(f"✓ 课程已存在: {course.name} (代码: {course.code})")
        course_objects.append(course)
    
    return course_objects


def add_students():
    """添加学生记录"""
    print("\n=== 添加学生记录 ===")
    student_objects = []
    
    for student_data in STUDENTS:
        # 检查学生是否已存在（通过学号）
        try:
            student = Student.objects.get(student_id=student_data['student_id'])
            print(f"⚠️  学生已存在: {student.name} (学号: {student.student_id})")
            student_objects.append(student)
        except Student.DoesNotExist:
            # 创建新学生
            student = Student.objects.create(**student_data)
            print(f"✓ 创建学生: {student.name} (学号: {student.student_id})")
            student_objects.append(student)
    
    return student_objects


def enroll_students_in_courses(students, courses):
    """为学生关联课程信息"""
    print("\n=== 为学生关联课程 ===")
    enrolled_count = 0
    
    for student in students:
        # 为每个学生随机选择2-4门课程
        num_courses = random.randint(2, 4)
        selected_courses = random.sample(courses, num_courses)
        
        for course in selected_courses:
            # 检查学生是否已经选修了这门课程
            try:
                Enrollment.objects.get(student=student, course=course)
                print(f"⚠️  {student.name} 已选修 {course.name}")
            except Enrollment.DoesNotExist:
                # 创建选课记录
                enrollment = Enrollment.objects.create(
                    student=student,
                    course=course,
                    # 随机生成过去30天内的选课日期
                    enroll_date=datetime.now() - timedelta(days=random.randint(1, 30)),
                    # 成绩暂时不设置，或者设置为None
                    score=None
                )
                enrolled_count += 1
                print(f"✓ {student.name} 选修 {course.name}")
    
    return enrolled_count


def main():
    """主函数"""
    print("开始执行添加学生记录并关联课程的操作...")
    
    # 1. 添加课程数据（如果不存在）
    courses = add_courses_if_not_exists()
    
    # 2. 添加学生记录
    students = add_students()
    
    # 3. 为学生关联课程信息
    enrolled_count = enroll_students_in_courses(students, courses)
    
    print(f"\n=== 操作完成 ===")
    print(f"成功添加 {len(students)} 名学生")
    print(f"成功关联 {enrolled_count} 条选课记录")


if __name__ == "__main__":
    main()