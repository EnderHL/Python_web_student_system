import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')
django.setup()

# 导入Course模型
from course.models import Course

# 尝试访问total_hours字段
def test_course_model():
    try:
        # 获取第一个课程对象
        course = Course.objects.first()
        if course:
            print(f"课程名称: {course.name}")
            print(f"尝试访问total_hours字段...")
            # 尝试访问total_hours属性
            hours = course.total_hours
            print(f"成功访问total_hours字段，值为: {hours}")
        else:
            print("数据库中没有课程数据，但模型可以正常导入")
    except AttributeError as e:
        print(f"访问total_hours字段失败: {e}")
    except Exception as e:
        print(f"发生其他错误: {e}")

if __name__ == "__main__":
    test_course_model()