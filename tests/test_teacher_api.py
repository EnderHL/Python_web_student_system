import os
import requests
import json

# API基础URL
BASE_URL = 'http://127.0.0.1:8000/api/'

# 测试教师列表API
def test_teacher_list():
    print("=== 测试教师列表API ===")
    
    try:
        # 先尝试登录获取token
        login_data = {
            'username': 'root',
            'password': 'root123456'
        }
        
        login_response = requests.post(
            f'{BASE_URL}auth/login/',
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get('tokens', {}).get('access')
            print("✅ 登录成功，获取到token")
            
            # 使用token请求教师列表
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            teachers_response = requests.get(
                f'{BASE_URL}teachers/',
                headers=headers,
                timeout=5
            )
            
            print(f"教师列表API响应状态码: {teachers_response.status_code}")
            print(f"教师列表API响应内容: {teachers_response.text}")
            
            if teachers_response.status_code == 200:
                teachers_data = teachers_response.json()
                print(f"✅ 成功获取教师列表，共{len(teachers_data)}名教师")
            else:
                print("❌ 获取教师列表失败")
        else:
            print(f"❌ 登录失败，状态码: {login_response.status_code}")
            print(f"登录响应内容: {login_response.text}")
            
            # 尝试不使用token直接访问
            print("\n尝试不使用token直接访问教师列表...")
            no_auth_response = requests.get(
                f'{BASE_URL}teachers/',
                timeout=5
            )
            print(f"无认证访问状态码: {no_auth_response.status_code}")
            print(f"无认证访问响应内容: {no_auth_response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        print("请确保Django服务器正在运行！")

# 检查数据库中是否有教师记录
def check_teacher_database():
    print("\n=== 检查数据库中的教师记录 ===")
    try:
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')
        import django
        django.setup()
        from teacher.models import Teacher
        
        teachers = Teacher.objects.all()
        print(f"数据库中共有{len(teachers)}名教师记录")
        for teacher in teachers[:5]:  # 只显示前5个
            print(f"- ID: {teacher.id}, 姓名: {teacher.name}, 邮箱: {teacher.email}")
            
    except Exception as e:
        print(f"❌ 检查数据库失败: {e}")

def main():
    test_teacher_list()
    check_teacher_database()
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    main()