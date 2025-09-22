import sys
import os

# 设置DJANGO_SETTINGS_MODULE环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django
from django.utils import timezone

# 初始化Django环境
django.setup()

from course.models import Course, Enrollment, TeachingAssignment, Classroom, Schedule
from student.models import Student
from teacher.models import Teacher
from user_auth.models import CustomUser


class CourseAdvancedFeaturesTester:
    """课程高级功能测试器"""
    
    def __init__(self):
        """初始化测试器"""
        print("\n===== 课程管理模块高级功能测试 =====\n")
        self.courses = []
        self.classrooms = []
        self.schedules = []
    
    def prepare_test_data(self):
        """准备测试数据"""
        print("1. 准备测试数据...")
        
        # 获取现有学生和教师数据
        try:
            self.students = Student.objects.all()[:3]
            self.teachers = Teacher.objects.all()[:2]
            
            if not self.students.exists():
                print("警告: 没有找到学生数据，将创建测试学生")
                self._create_test_students()
                self.students = Student.objects.all()[:3]
            
            if not self.teachers.exists():
                print("警告: 没有找到教师数据，将创建测试教师")
                self._create_test_teachers()
                self.teachers = Teacher.objects.all()[:2]
            
        except Exception as e:
            print(f"准备测试数据时出错: {e}")
            self._create_test_students()
            self._create_test_teachers()
            self.students = Student.objects.all()[:3]
            self.teachers = Teacher.objects.all()[:2]
    
    def _create_test_students(self):
        """创建测试学生"""
        for i in range(3):
            Student.objects.create(
                name=f"测试学生{i+1}",
                age=20 + i,
                gender='male' if i % 2 == 0 else 'female',
                student_id=f"2024000{i+1}",
                email=f"test_student{i+1}@example.com",
                phone=f"138001380{i+1}1"
            )
        print("已创建3名测试学生")
    
    def _create_test_teachers(self):
        """创建测试教师"""
        for i in range(2):
            user = CustomUser.objects.create_user(
                username=f"teacher{i+1}",
                password="password123",
                email=f"teacher{i+1}@example.com"
            )
            Teacher.objects.create(
                user=user,
                name=f"测试教师{i+1}",
                age=35 + i * 5,
                gender='male' if i % 2 == 0 else 'female',
                email=f"teacher{i+1}@example.com"
            )
        print("已创建2名测试教师")
    
    def test_course_types(self):
        """测试课程类型功能"""
        print("\n2. 测试课程类型功能...")
        
        # 创建必修课
        required_course = Course.objects.create(
            name="高等数学",
            code="MATH101",
            credits=4.0,
            description="大学基础课程",
            total_hours=64,
            semester="2024-2025学年第一学期",
            course_type='required',  # 必修课
            max_students=120
        )
        self.courses.append(required_course)
        print(f"创建必修课: {required_course.name} ({required_course.get_course_type_display()})")
        
        # 创建选修课
        elective_course = Course.objects.create(
            name="人工智能导论",
            code="CS102",
            credits=3.0,
            description="计算机科学选修课程",
            total_hours=48,
            semester="2024-2025学年第一学期",
            course_type='elective',  # 选修课
            max_students=80
        )
        self.courses.append(elective_course)
        print(f"创建选修课: {elective_course.name} ({elective_course.get_course_type_display()})")
        
        # 验证课程类型
        required_courses = Course.objects.filter(course_type='required')
        elective_courses = Course.objects.filter(course_type='elective')
        
        print(f"\n当前必修课数量: {required_courses.count()}")
        print(f"当前选修课数量: {elective_courses.count()}")
    
    def test_classroom_management(self):
        """测试教室管理功能"""
        print("\n3. 测试教室管理功能...")
        
        # 创建不同类型的教室
        classrooms_data = [
            {
                'name': 'A101',
                'location': '第一教学楼1层',
                'capacity': 60,
                'equipment': '投影仪、白板'
            },
            {
                'name': 'B202',
                'location': '第二教学楼2层',
                'capacity': 80,
                'equipment': '投影仪、白板、音响系统'
            },
            {
                'name': 'C303',
                'location': '第三教学楼3层',
                'capacity': 40,
                'equipment': '投影仪、白板、多媒体讲台'
            }
        ]
        
        for data in classrooms_data:
            classroom = Classroom.objects.create(**data)
            self.classrooms.append(classroom)
            print(f"创建教室: {classroom.name}, 位置: {classroom.location}, 容量: {classroom.capacity}")
        
        # 验证教室数据
        all_classrooms = Classroom.objects.all()
        print(f"\n总教室数量: {all_classrooms.count()}")
    
    def test_schedule_management(self):
        """测试排课功能"""
        print("\n4. 测试排课功能...")
        
        # 确保有课程和教室数据
        if not self.courses:
            print("警告: 没有课程数据，将创建测试课程")
            self.test_course_types()
        
        if not self.classrooms:
            print("警告: 没有教室数据，将创建测试教室")
            self.test_classroom_management()
        
        # 创建授课记录
        teaching_assignments = []
        for teacher in self.teachers:
            for course in self.courses:
                assignment = TeachingAssignment.objects.create(
                    teacher=teacher,
                    course=course,
                    teaching_hours=course.total_hours // 2 if len(self.teachers) > 1 else course.total_hours
                )
                teaching_assignments.append(assignment)
                print(f"创建授课记录: {teacher.name} - {course.name}")
        
        # 创建排课记录（包括单周、双周和每周模式）
        schedule_data = [
            {
                'course': self.courses[0],
                'classroom': self.classrooms[0],
                'teaching_assignment': teaching_assignments[0],
                'day_of_week': 1,  # 周一
                'start_section': 1,
                'end_section': 2,
                'week_pattern': 'all'  # 每周
            },
            {
                'course': self.courses[0],
                'classroom': self.classrooms[0],
                'teaching_assignment': teaching_assignments[0],
                'day_of_week': 3,  # 周三
                'start_section': 3,
                'end_section': 4,
                'week_pattern': 'odd'  # 单周
            },
            {
                'course': self.courses[1],
                'classroom': self.classrooms[1],
                'teaching_assignment': teaching_assignments[2],
                'day_of_week': 2,  # 周二
                'start_section': 5,
                'end_section': 6,
                'week_pattern': 'even'  # 双周
            }
        ]
        
        for data in schedule_data:
            schedule = Schedule.objects.create(**data)
            self.schedules.append(schedule)
            week_pattern_text = schedule.get_week_pattern_display()
            print(f"创建排课记录: {schedule.course.name} - {schedule.classroom.name} - 星期{schedule.day_of_week} - {week_pattern_text}")
        
        # 验证排课数据
        all_schedules = Schedule.objects.all()
        print(f"\n总排课记录数量: {all_schedules.count()}")
        
        # 按上课周模式统计
        weekly_schedules = Schedule.objects.filter(week_pattern='all')
        odd_week_schedules = Schedule.objects.filter(week_pattern='odd')
        even_week_schedules = Schedule.objects.filter(week_pattern='even')
        
        print(f"每周排课数量: {weekly_schedules.count()}")
        print(f"单周排课数量: {odd_week_schedules.count()}")
        print(f"双周排课数量: {even_week_schedules.count()}")
    
    def test_enrollment_with_course_types(self):
        """测试按课程类型选课功能"""
        print("\n5. 测试按课程类型选课功能...")
        
        # 获取必修课和选修课
        required_courses = Course.objects.filter(course_type='required')
        elective_courses = Course.objects.filter(course_type='elective')
        
        # 为学生选课
        for student in self.students:
            # 每个学生选1门必修课
            if required_courses.exists():
                course = required_courses.first()
                Enrollment.objects.create(
                    student=student,
                    course=course,
                    enroll_date=timezone.now()
                )
                print(f"学生 {student.name} 选择必修课: {course.name}")
            
            # 每个学生选1门选修课
            if elective_courses.exists():
                course = elective_courses.first()
                Enrollment.objects.create(
                    student=student,
                    course=course,
                    enroll_date=timezone.now()
                )
                print(f"学生 {student.name} 选择选修课: {course.name}")
        
        # 统计选课情况
        total_enrollments = Enrollment.objects.count()
        required_enrollments = Enrollment.objects.filter(course__course_type='required').count()
        elective_enrollments = Enrollment.objects.filter(course__course_type='elective').count()
        
        print(f"\n总选课记录数量: {total_enrollments}")
        print(f"必修课选课数量: {required_enrollments}")
        print(f"选修课选课数量: {elective_enrollments}")
    
    def run_all_tests(self):
        """运行所有测试"""
        try:
            # 准备测试数据
            self.prepare_test_data()
            
            # 运行各项测试
            self.test_course_types()
            self.test_classroom_management()
            self.test_schedule_management()
            self.test_enrollment_with_course_types()
            
            print("\n===== 所有测试完成 =====")
            return True
        except Exception as e:
            print(f"\n测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == '__main__':
    # 运行数据库迁移命令
    print("开始执行数据库迁移...")
    os.system(f"cd {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))} && python manage.py makemigrations")
    os.system(f"cd {os.path.dirname(os.path.dirname(os.path.abspath(__file__)))} && python manage.py migrate")
    
    # 运行测试
    tester = CourseAdvancedFeaturesTester()
    success = tester.run_all_tests()
    
    if success:
        print("课程管理模块高级功能测试成功！")
    else:
        print("课程管理模块高级功能测试失败，请检查错误信息。")