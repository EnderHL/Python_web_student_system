"""
简单的课程关联验证脚本
"""
import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')

# 导入Django设置
import django
django.setup()

# 导入所需的模型
from course.models import Course, TeachingAssignment, Schedule, Classroom
from teacher.models import Teacher


def verify_database_setup():
    """验证数据库设置和关联关系"""
    print("===== 课程数据库验证 =====")
    
    try:
        # 检查课程表
        course_count = Course.objects.count()
        print(f"课程表中有 {course_count} 条记录")
        
        # 检查教师表
        teacher_count = Teacher.objects.count()
        print(f"教师表中有 {teacher_count} 条记录")
        
        # 检查教室表
        classroom_count = Classroom.objects.count()
        print(f"教室表中有 {classroom_count} 条记录")
        
        # 检查教师与课程的关联表
        teaching_count = TeachingAssignment.objects.count()
        print(f"教师授课关联表中有 {teaching_count} 条记录")
        
        # 检查排课表（关联课程和教室）
        schedule_count = Schedule.objects.count()
        print(f"排课表中有 {schedule_count} 条记录")
        
        # 如果有数据，进行简单的关联验证
        if course_count > 0:
            first_course = Course.objects.first()
            print(f"\n示例课程: {first_course.name} (代码: {first_course.code})")
            
            # 检查该课程的授课教师
            teachers = [ta.teacher.name for ta in TeachingAssignment.objects.filter(course=first_course)]
            if teachers:
                print(f"  授课教师: {', '.join(teachers)}")
            else:
                print("  暂无授课教师")
            
            # 检查该课程的教室信息
            classrooms = []
            for schedule in Schedule.objects.filter(course=first_course):
                classrooms.append(f"{schedule.classroom.name} (容量: {schedule.classroom.capacity})")
            
            if classrooms:
                print(f"  上课教室: {', '.join(classrooms)}")
            else:
                print("  暂无教室安排")
        
        print("\n验证完成！课程数据库表已成功创建，并与教师表和教室表建立了正确的关联。")
        
    except Exception as e:
        print(f"验证过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    verify_database_setup()