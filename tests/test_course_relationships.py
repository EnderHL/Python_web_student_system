"""
课程关联关系测试脚本
用于验证课程与教师、教室的关联是否正常工作
"""
from course.models import Course, TeachingAssignment, Schedule
from teacher.models import Teacher
from classroom.models import Classroom


def test_course_teacher_relationship():
    """测试课程与教师的关联关系"""
    print("===== 测试课程与教师的关联关系 =====")
    
    # 获取所有课程
    courses = Course.objects.all()
    
    if not courses.exists():
        print("没有找到课程数据")
        return
    
    for course in courses[:3]:  # 只测试前3个课程
        print(f"\n课程: {course.name} (代码: {course.code})")
        
        # 获取教授该课程的教师
        try:
            teaching_assignments = TeachingAssignment.objects.filter(course=course)
            
            if teaching_assignments.exists():
                print(f"  授课教师:")
                for assignment in teaching_assignments:
                    print(f"    - {assignment.teacher.name} (职称: {assignment.teacher.title})")
                    print(f"      授课课时: {assignment.teaching_hours}")
            else:
                print("  暂无教师授课记录")
        except Exception as e:
            print(f"  获取教师信息时出错: {str(e)}")


def test_course_classroom_relationship():
    """测试课程与教室的关联关系"""
    print("\n===== 测试课程与教室的关联关系 =====")
    
    # 获取所有课程
    courses = Course.objects.all()
    
    if not courses.exists():
        print("没有找到课程数据")
        return
    
    for course in courses[:3]:  # 只测试前3个课程
        print(f"\n课程: {course.name} (代码: {course.code})")
        
        # 获取该课程的排课记录和教室信息
        try:
            schedules = Schedule.objects.filter(course=course)
            
            if schedules.exists():
                print(f"  排课信息:")
                for schedule in schedules:
                    print(f"    - 教室: {schedule.classroom.name} (位置: {schedule.classroom.location})")
                    print(f"      教室容量: {schedule.classroom.capacity}")
                    print(f"      上课时间: 星期{schedule.day_of_week}, {schedule.start_section}-{schedule.end_section}节")
                    print(f"      上课模式: {schedule.get_week_pattern_display()}")
                    print(f"      授课教师: {schedule.teaching_assignment.teacher.name}")
            else:
                print("  暂无排课记录")
        except Exception as e:
            print(f"  获取教室信息时出错: {str(e)}")


def verify_teacher_teaches_course(teacher_id, course_id):
    """验证指定教师是否教授指定课程"""
    print(f"\n===== 验证教师(ID:{teacher_id})是否教授课程(ID:{course_id}) =====")
    
    try:
        teacher = Teacher.objects.get(id=teacher_id)
        course = Course.objects.get(id=course_id)
        
        # 检查是否存在授课记录
        exists = TeachingAssignment.objects.filter(teacher=teacher, course=course).exists()
        
        if exists:
            print(f"✓ 教师 {teacher.name} 确实教授课程 {course.name}")
        else:
            print(f"✗ 教师 {teacher.name} 不教授课程 {course.name}")
            
    except Teacher.DoesNotExist:
        print(f"错误: 找不到ID为{teacher_id}的教师")
    except Course.DoesNotExist:
        print(f"错误: 找不到ID为{course_id}的课程")
    except Exception as e:
        print(f"验证过程中出错: {str(e)}")


def check_classroom_capacity_for_course(course_id):
    """检查课程对应的教室容量"""
    print(f"\n===== 检查课程(ID:{course_id})对应的教室容量 =====")
    
    try:
        course = Course.objects.get(id=course_id)
        
        # 获取该课程的所有排课记录
        schedules = Schedule.objects.filter(course=course)
        
        if schedules.exists():
            print(f"课程 {course.name} 的排课教室信息:")
            for schedule in schedules:
                print(f"- 教室: {schedule.classroom.name}")
                print(f"  容量: {schedule.classroom.capacity}")
                print(f"  当前选课人数: {course.enrollments.count()}")
                print(f"  课程最大人数限制: {course.max_students}")
                
                # 检查教室容量是否满足课程需求
                if schedule.classroom.capacity >= course.max_students:
                    print("  ✓ 教室容量满足课程需求")
                else:
                    print(f"  ✗ 警告: 教室容量({schedule.classroom.capacity})小于课程最大人数限制({course.max_students})")
        else:
            print(f"课程 {course.name} 暂无排课记录")
            print(f"课程最大人数限制: {course.max_students}")
            
    except Course.DoesNotExist:
        print(f"错误: 找不到ID为{course_id}的课程")
    except Exception as e:
        print(f"检查过程中出错: {str(e)}")


def main():
    """主函数"""
    print("开始测试课程关联关系...\n")
    
    # 测试基本关联关系
    test_course_teacher_relationship()
    test_course_classroom_relationship()
    
    # 验证特定教师是否教授特定课程
    # 注意：这里使用的ID需要根据实际数据库中的数据进行调整
    if Teacher.objects.exists() and Course.objects.exists():
        first_teacher = Teacher.objects.first()
        first_course = Course.objects.first()
        verify_teacher_teaches_course(first_teacher.id, first_course.id)
        
        # 检查课程对应的教室容量
        check_classroom_capacity_for_course(first_course.id)
    
    print("\n测试完成!")


if __name__ == "__main__":
    main()