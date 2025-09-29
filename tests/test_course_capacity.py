from django.test import TestCase
from course.models import Course, Enrollment
from student.models import Student
from django.core.exceptions import ValidationError

class CourseCapacityTest(TestCase):
    def test_online_course_capacity(self):
        """测试线上课程自动设置固定容量1000"""
        # 创建一个线上课程
        online_course = Course.objects.create(
            name="Python网络编程",
            code="CS102",
            credits=3.0,
            total_hours=48,
            semester="2024-2025学年第一学期",
            teaching_method="online",
            course_type="elective"
        )
        
        # 验证线上课程的max_students被自动设置为1000
        self.assertEqual(online_course.max_students, 1000, "线上课程容量应该为1000")
        
        # 测试修改课程为线下后，容量不会自动改变
        online_course.teaching_method = "offline"
        online_course.save()
        original_capacity = online_course.max_students
        self.assertEqual(original_capacity, 1000, "修改为线下课程后容量不应改变")
        
        # 测试再改回线上，容量会自动设置为1000
        online_course.teaching_method = "online"
        online_course.save()
        self.assertEqual(online_course.max_students, 1000, "改回线上课程后容量应该为1000")
    
    def test_student_enrollment_capacity(self):
        """测试学生选课人数校验逻辑"""
        # 创建一个容量为5的线下课程用于测试
        test_course = Course.objects.create(
            name="数据结构实验",
            code="CS002",
            credits=1.5,
            total_hours=24,
            semester="2024-2025学年第一学期",
            teaching_method="offline",
            course_type="required",
            max_students=5
        )
        
        # 创建6名学生用于测试
        students = []
        for i in range(6):
            student = Student.objects.create(
                name=f"测试学生{i+1}",
                age=20 + i % 3,
                gender='male' if i % 2 == 0 else 'female',
                student_id=f"2024000{i+1}",
                class_name=f"计科24{i//2+1}班",
                college="计算机学院",
                major="计算机科学与技术",
                email=f"student{i+1}@example.com"
            )
            students.append(student)
        
        # 导入序列化器
        from course.serializers import EnrollmentSerializer
        
        # 前5名学生应该能成功选课
        for i in range(5):
            data = {'student': students[i].id, 'course': test_course.id}
            serializer = EnrollmentSerializer(data=data)
            self.assertTrue(serializer.is_valid(), f"学生{students[i].name}选课应该成功")
            serializer.save()
        
        # 验证当前选课人数
        current_count = Enrollment.objects.filter(course=test_course).count()
        self.assertEqual(current_count, 5, "当前选课人数应该等于课程最大容量")
        
        # 尝试让第6名学生选课（应该失败，因为已经达到容量上限）
        data = {'student': students[5].id, 'course': test_course.id}
        serializer = EnrollmentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('该课程选课人数已达上限', str(serializer.errors))