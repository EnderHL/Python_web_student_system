#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
添加课程测试数据脚本
向course表添加20条与其他表(教师、教室)相关联的数据
"""
import os
import sys
import random
from datetime import datetime, timedelta

# 添加Django项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')

# 导入Django模块并初始化
import django
django.setup()

# 导入模型
from course.models import Course, Classroom, TeachingAssignment
from teacher.models import Teacher
from user_auth.models import CustomUser


class CourseDataGenerator:
    """课程数据生成器"""
    
    def __init__(self):
        # 生成随机数据的基础材料
        self.course_names = [
            "高等数学", "线性代数", "概率论与数理统计", "大学物理", "大学英语",
            "计算机基础", "程序设计基础", "数据结构与算法", "操作系统", "计算机网络",
            "数据库原理", "软件工程", "人工智能导论", "机器学习", "深度学习",
            "云计算技术", "大数据分析", "网络安全", "计算机组成原理", "数字电路"
        ]
        
        self.departments = ["计算机科学与技术", "软件工程", "人工智能", "数据科学", "电子工程", "自动化"]
        self.classroom_locations = ["第一教学楼", "第二教学楼", "实验楼A座", "实验楼B座", "综合教学楼"]
        self.semesters = ["2024-2025学年第一学期", "2024-2025学年第二学期"]
        
        # 确保有可用的教师和教室数据
        self.ensure_related_data_exists()
    
    def ensure_related_data_exists(self):
        """确保有可用的教师和教室数据，如果没有则创建"""
        # 检查教师数据
        if Teacher.objects.count() == 0:
            print("没有找到教师数据，正在创建教师测试数据...")
            self.create_teachers()
        else:
            print(f"找到{Teacher.objects.count()}名教师数据")
        
        # 检查教室数据
        if Classroom.objects.count() == 0:
            print("没有找到教室数据，正在创建教室测试数据...")
            self.create_classrooms()
        else:
            print(f"找到{Classroom.objects.count()}间教室数据")
    
    def create_teachers(self):
        """创建教师测试数据"""
        # 先创建CustomUser账户
        user_names = [f"teacher{i}" for i in range(1, 11)]
        teachers = []
        
        for i, username in enumerate(user_names, 1):
            # 检查用户是否存在
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': f"teacher{i}@example.com",
                    'is_staff': True,
                    'is_teacher': True
                }
            )
            if created:
                # 如果用户是新创建的，设置密码
                user.set_password('123456')
                user.save()
                
            # 创建教师信息
            teacher = Teacher(
                user=user,
                name=f"教师{i}",
                age=random.randint(28, 60),
                gender=random.choice(['男', '女']),
                title=random.choice(['助教', '讲师', '副教授', '教授']),
                department=random.choice(self.departments),
                email=f"teacher{i}@example.com",
                phone=f"1380013800{i}",
                hire_date=datetime.now() - timedelta(days=random.randint(365, 10950))  # 1-30年
            )
            teachers.append(teacher)
        
        Teacher.objects.bulk_create(teachers)
        print(f"创建了{len(teachers)}名教师数据")
    
    def create_classrooms(self):
        """创建教室测试数据"""
        classrooms = []
        
        # 创建线上课程对应的"虚拟教室"
        online_classroom = Classroom(
            name="线上教室",
            location="线上",
            capacity=1000,
            equipment="线上直播平台"
        )
        classrooms.append(online_classroom)
        
        # 创建线下教室
        for i in range(1, 21):
            classroom = Classroom(
                name=f"{random.choice(self.classroom_locations)}-{random.randint(101, 505)}",
                location=random.choice(self.classroom_locations),
                capacity=random.choice([30, 40, 50, 60, 80, 100]),
                equipment=random.choice(["投影仪", "电脑", "白板", "投影仪+电脑", "投影仪+白板+电脑"])
            )
            classrooms.append(classroom)
        
        Classroom.objects.bulk_create(classrooms)
        print(f"创建了{len(classrooms)}间教室数据")
    
    def generate_course_code(self, index):
        """生成唯一的课程代码"""
        prefix = random.choice(["CS", "MATH", "PHYS", "ENGL", "ELEC", "AI"])
        
        # 生成基础代码
        base_code = f"{prefix}{2024}{index:03d}"
        
        # 检查代码是否已存在，如果存在则添加随机数后缀
        while Course.objects.filter(code=base_code).exists():
            # 添加1-3位随机数作为后缀
            random_suffix = random.randint(10, 999)
            base_code = f"{prefix}{2024}{index:03d}_{random_suffix}"
        
        return base_code
    
    def generate_courses(self, count=20):
        """生成课程数据"""
        # 获取所有教师和教室
        teachers = list(Teacher.objects.all())
        classrooms = list(Classroom.objects.all())
        
        # 确保有足够的教师和教室
        if not teachers or not classrooms:
            print("错误：缺少必要的教师或教室数据")
            return
        
        # 获取当前已有的课程数量，用于生成唯一的课程代码
        existing_count = Course.objects.count()
        
        courses = []
        
        for i in range(count):
            # 使用现有课程数量+1作为索引，避免代码重复
            index = existing_count + i + 1
            
            # 随机选择授课方式
            teaching_method = random.choice(['online', 'offline'])
            
            # 根据授课方式选择教室
            if teaching_method == 'online':
                # 线上课程选择线上教室
                classroom = next((c for c in classrooms if "线上" in c.name), None)
                if not classroom:
                    classroom = random.choice(classrooms)
            else:
                # 线下课程选择普通教室
                classroom = random.choice([c for c in classrooms if "线上" not in c.name])
            
            # 创建课程
            course = Course(
                name=self.course_names[i],  # 使用预定义的课程名称
                code=self.generate_course_code(index),
                course_type=random.choice(['required', 'elective']),
                teaching_method=teaching_method,
                credits=random.choice([1.0, 1.5, 2.0, 2.5, 3.0]),
                total_hours=random.choice([32, 48, 64, 80]),
                classroom=classroom if teaching_method == 'offline' else None,
                semester=random.choice(self.semesters),
                description=f"这是一门关于{self.course_names[i]}的课程，适合{random.choice(['本科生', '研究生', '全体学生'])}学习。"
            )
            courses.append(course)
        
        # 批量创建课程
        Course.objects.bulk_create(courses)
        print(f"创建了{len(courses)}门课程数据")
        
        # 重新获取课程对象，确保它们已经被保存
        courses = Course.objects.order_by('-id')[:count]
        
        # 创建教师授课关联
        course_teacher_assignments = []
        for course in courses:
            # 每门课程分配1-2名教师
            assigned_teachers = random.sample(teachers, random.randint(1, 2))
            
            for teacher in assigned_teachers:
                assignment = TeachingAssignment(
                    teacher=teacher,
                    course=course,
                    teaching_hours=course.total_hours // len(assigned_teachers)  # 平均分配课时
                )
                course_teacher_assignments.append(assignment)
        
        # 批量创建教师授课关联
        TeachingAssignment.objects.bulk_create(course_teacher_assignments)
        print(f"创建了{len(course_teacher_assignments)}条教师授课关联数据")
    
    def run(self):
        """运行数据生成器"""
        print("开始生成课程测试数据...")
        self.generate_courses()
        print("课程测试数据生成完成！")


if __name__ == "__main__":
    generator = CourseDataGenerator()
    generator.run()