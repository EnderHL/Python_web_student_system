import unittest
import threading
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user_auth.models import CustomUser
from course.models import Course, Enrollment, Classroom
from student.models import Student
from django.db import transaction

class ConcurrentEnrollmentTest(TestCase):
    """
    测试并发选课场景，确保在高并发情况下课程容量限制依然有效
    """
    def setUp(self):
        """
        设置测试数据
        """
        # 创建测试用户和客户端
        self.client = APIClient()
        
        # 在Django REST Framework测试中，需要创建一个有权限的用户并使用force_authenticate进行认证
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # 创建一个线下课程，容量设置为5
        self.classroom = Classroom.objects.create(
            name='测试教室',
            location='测试位置',
            capacity=5
        )
        
        # 创建一个线下课程，容量为5
        self.course = Course.objects.create(
            name='测试课程',
            code='TEST001',
            credits=3,
            teaching_method='offline',
            max_students=5,  # 故意设置较小的容量以便测试并发情况
            total_hours=48,
            semester='2023-2024-1'
        )
        
        # 创建10个学生用于测试
        self.students = []
        for i in range(10):
            student = Student.objects.create(
                name=f'学生{i}',
                student_id=f'STD{i:03d}',
                major='测试专业',
                email=f'student{i}@example.com',
                age=20,
                gender='男',
                class_name=f'测试班级{i}',
                college='测试学院',
                phone=f'1380013800{i}'
            )
            self.students.append(student)
    
    def test_concurrent_enrollment(self):
        """
        测试课程容量限制功能，确保不会超过课程容量
        由于Django测试的事务隔离机制，我们不使用多线程，而是通过多次调用API来验证
        """
        # 尝试让所有10个学生选课
        results = []
        for student in self.students:
            data = {
                'student': student.id,
                'course': self.course.id,
                'semester': '2023-2024-1'
            }
            response = self.client.post(reverse('enrollment-list'), data, format='json')
            results.append(response.status_code)
        
        # 验证最终选课人数不超过课程容量
        final_enrollments = Enrollment.objects.filter(course=self.course).count()
        self.assertEqual(final_enrollments, self.course.max_students, 
                         f"课程容量限制失败，实际选课人数：{final_enrollments}，最大容量：{self.course.max_students}")
        
        # 验证成功和失败的请求数量
        success_count = results.count(status.HTTP_201_CREATED)
        self.assertEqual(success_count, self.course.max_students)
        
        error_count = results.count(status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_count, len(self.students) - self.course.max_students)
    
    def test_duplicate_enrollment(self):
        """
        测试同一个学生重复选课的情况
        """
        # 首先让学生选课成功
        student = self.students[0]
        data = {
            'student': student.id,
            'course': self.course.id,
            'semester': '2023-2024-1'
        }
        response = self.client.post(reverse('enrollment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 尝试再次选课，应该失败
        response = self.client.post(reverse('enrollment-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # 检查错误信息
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0].code, 'unique')
    
    def tearDown(self):
        """
        清理测试数据
        """
        Enrollment.objects.all().delete()
        Student.objects.all().delete()
        Course.objects.all().delete()
        Classroom.objects.all().delete()

if __name__ == '__main__':
    unittest.main()