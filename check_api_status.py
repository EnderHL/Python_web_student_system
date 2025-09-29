import os
import sys
import requests
import time
from django.db import connection
from django.core.management import execute_from_command_line

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')

# 尝试导入Django设置
try:
    import django
django.setup()
    print("✅ Django环境已成功初始化")
except Exception as e:
    print(f"❌ 初始化Django环境失败: {e}")
    print("请确保在项目根目录下运行此脚本")
    sys.exit(1)

# 检查数据库连接
def check_database():
    try:
        with connection.cursor() as cursor:
            # 检查课程表是否存在
            cursor.execute("""SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'course_course'
            );""")
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                print("❌ 课程表(course_course)不存在")
                return False
            
            # 检查课程数据
            cursor.execute("SELECT COUNT(*) FROM course_course;")
            course_count = cursor.fetchone()[0]
            print(f"✅ 数据库连接正常")
            print(f"✅ 课程表中共有 {course_count} 条课程数据")
            
            # 检查教师表
            cursor.execute("""SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'teacher_teacher'
            );""")
            teacher_table_exists = cursor.fetchone()[0]
            
            if teacher_table_exists:
                cursor.execute("SELECT COUNT(*) FROM teacher_teacher;")
                teacher_count = cursor.fetchone()[0]
                print(f"✅ 教师表中共有 {teacher_count} 条教师数据")
            
            # 检查教室表
            cursor.execute("""SELECT EXISTS (
                SELECT 1 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'course_classroom'
            );""")
            classroom_table_exists = cursor.fetchone()[0]
            
            if classroom_table_exists:
                cursor.execute("SELECT COUNT(*) FROM course_classroom;")
                classroom_count = cursor.fetchone()[0]
                print(f"✅ 教室表中共有 {classroom_count} 条教室数据")
            
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

# 检查后端服务器是否运行
def check_server():
    try:
        url = "http://localhost:8000/api"
        response = requests.get(url, timeout=5)
        print(f"✅ 后端服务器正在运行: {url} (状态码: {response.status_code})")
        return True
    except requests.ConnectionError:
        print("❌ 后端服务器未运行，请先启动服务器")
        print("请运行命令: python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ 检查服务器状态时出错: {e}")
        return False

# 检查API端点
def check_api_endpoints():
    endpoints = [
        "/courses/",
        "/teachers/",
        "/classrooms/",
        "/auth/profile/"
    ]
    
    print("\n正在检查API端点可用性...")
    
    for endpoint in endpoints:
        url = f"http://localhost:8000/api{endpoint}"
        try:
            response = requests.get(url, timeout=3)
            print(f"API端点: {url}")
            print(f"  状态码: {response.status_code}")
            print(f"  响应内容长度: {len(response.text)} 字节")
            # 如果是401未授权，这是正常的，因为我们没有提供token
            if response.status_code == 401:
                print("  提示: 此端点需要认证")
        except Exception as e:
            print(f"API端点: {url} 不可访问: {e}")

# 主函数
def main():
    print("\n===== 学生管理系统API状态检查 =====")
    
    # 检查数据库
    db_ok = check_database()
    
    # 检查服务器
    server_ok = check_server()
    
    # 如果服务器运行正常，检查API端点
    if server_ok:
        check_api_endpoints()
    
    print("\n===== 测试指南 =====")
    print("1. 确保后端服务器正在运行: python manage.py runserver")
    print("2. 确保前端开发服务器正在运行: 在frontend目录下运行 npm run dev")
    print("3. 打开浏览器，访问测试页面: ")
    print("   http://localhost:5173/test_api_course.html")
    print("4. 在测试页面中，先点击'设置临时测试Token'")
    print("5. 然后点击各种API测试按钮，查看结果")
    print("\n如果遇到401错误，请检查Token设置是否正确")
    print("如果遇到404错误，请检查API端点是否正确")
    print("如果遇到500错误，请检查后端服务器日志")

if __name__ == "__main__":
    main()