"""
教师模块认证集成测试脚本
测试教师用户注册、登录、访问教师API以及角色管理功能
"""
import requests
import json
import time

# 基础URL配置
base_url = 'http://localhost:8000/api'

# 教师用户注册数据
teacher_registration_data = {
    "username": f"teacher_{int(time.time())}",
    "email": f"teacher_{int(time.time())}@example.com",
    "password": "Teacher@123",
    "password2": "Teacher@123",
    "first_name": "张",
    "last_name": "老师",
    "user_type": "teacher",
    "phone_number": "13800138001"
}

# 管理员用户数据（用于角色管理测试）
admin_credentials = {
    "username": "admin",
    "password": "Admin@123"
}

print("===== 教师模块认证集成测试开始 =====")

# 1. 教师用户注册
try:
    print("\n1. 测试教师用户注册...")
    register_url = f"{base_url}/auth/register/"
    response = requests.post(register_url, json=teacher_registration_data)
    response_data = response.json()
    
    if response.status_code == 201:
        print("✅ 教师用户注册成功")
        print(f"   用户名: {response_data['user']['username']}")
        print(f"   邮箱: {response_data['user']['email']}")
        print(f"   用户类型: {response_data['user']['user_type_display']}")
        
        # 保存注册成功的教师用户信息
        teacher_username = teacher_registration_data['username']
        teacher_password = teacher_registration_data['password']
    else:
        print(f"❌ 教师用户注册失败: {response_data}")
        exit()
except Exception as e:
    print(f"❌ 教师用户注册过程发生错误: {str(e)}")
    exit()

# 2. 教师用户登录
try:
    print("\n2. 测试教师用户登录...")
    login_url = f"{base_url}/auth/login/"
    login_data = {
        "username": teacher_username,
        "password": teacher_password
    }
    response = requests.post(login_url, json=login_data)
    response_data = response.json()
    
    if response.status_code == 200:
        print("✅ 教师用户登录成功")
        print(f"   用户ID: {response_data['user']['id']}")
        print(f"   用户类型: {response_data['user']['user_type_display']}")
        
        # 保存登录凭证
        teacher_access_token = response_data['tokens']['access']
        teacher_refresh_token = response_data['tokens']['refresh']
        
        # 设置认证头
        teacher_headers = {
            'Authorization': f'Bearer {teacher_access_token}',
            'Content-Type': 'application/json'
        }
    else:
        print(f"❌ 教师用户登录失败: {response_data}")
        exit()
except Exception as e:
    print(f"❌ 教师用户登录过程发生错误: {str(e)}")
    exit()

# 3. 管理员用户登录（用于角色管理测试）
try:
    print("\n3. 测试管理员用户登录...")
    response = requests.post(login_url, json=admin_credentials)
    response_data = response.json()
    
    if response.status_code == 200:
        print("✅ 管理员用户登录成功")
        print(f"   用户名: {response_data['user']['username']}")
        print(f"   用户类型: {response_data['user']['user_type_display']}")
        
        # 保存登录凭证
        admin_access_token = response_data['tokens']['access']
        
        # 设置认证头
        admin_headers = {
            'Authorization': f'Bearer {admin_access_token}',
            'Content-Type': 'application/json'
        }
    else:
        print(f"❌ 管理员用户登录失败: {response_data}")
        print("   注意：如果管理员账户不存在，角色管理测试将跳过")
        admin_headers = None
except Exception as e:
    print(f"❌ 管理员用户登录过程发生错误: {str(e)}")
    print("   注意：如果管理员账户不存在，角色管理测试将跳过")
    admin_headers = None

# 4. 创建教师资料
try:
    print("\n4. 测试创建教师资料...")
    teachers_url = f"{base_url}/teachers/"
    teacher_data = {
        "name": "张老师",
        "age": 35,
        "gender": "男",
        "title": "副教授",
        "department": "计算机科学系",
        "email": f"teacher_{int(time.time())}@example.com",
        "phone": "13800138001",
        "avatar": "https://example.com/avatar.jpg",
        "hire_date": "2020-01-01"
    }
    response = requests.post(teachers_url, json=teacher_data, headers=teacher_headers)
    response_data = response.json()
    
    if response.status_code == 201:
        print("✅ 教师资料创建成功")
        print(f"   教师ID: {response_data['id']}")
        print(f"   教师姓名: {response_data['name']}")
        print(f"   所属部门: {response_data['department']}")
        
        # 保存教师ID用于后续测试
        teacher_id = response_data['id']
    else:
        print(f"❌ 教师资料创建失败: {response_data}")
        # 即使创建失败，我们也继续测试其他功能
        teacher_id = None
except Exception as e:
    print(f"❌ 教师资料创建过程发生错误: {str(e)}")
    teacher_id = None

# 5. 获取教师列表（需要认证）
try:
    print("\n5. 测试获取教师列表（需要认证）...")
    response = requests.get(teachers_url, headers=teacher_headers)
    response_data = response.json()
    
    if response.status_code == 200:
        print(f"✅ 成功获取教师列表，共 {len(response_data)} 位教师")
        if len(response_data) > 0:
            print(f"   第一位教师: {response_data[0]['name']}")
    else:
        print(f"❌ 获取教师列表失败: {response_data}")
except Exception as e:
    print(f"❌ 获取教师列表过程发生错误: {str(e)}")

# 6. 角色管理测试（如果管理员已登录）
if admin_headers:
    try:
        print("\n6. 测试角色管理功能...")
        
        # 6.1 创建角色
        print("   6.1 创建新角色...")
        roles_url = f"{base_url}/roles/"
        role_data = {
            "name": f"course_manager_{int(time.time())}",
            "description": "课程管理员角色，可以管理课程信息"
        }
        response = requests.post(roles_url, json=role_data, headers=admin_headers)
        response_data = response.json()
        
        if response.status_code == 201:
            print("   ✅ 角色创建成功")
            print(f"      角色ID: {response_data['id']}")
            print(f"      角色名称: {response_data['name']}")
            
            # 保存角色ID用于后续测试
            role_id = response_data['id']
            
            # 6.2 为教师分配角色
            if teacher_id:
                print("   6.2 为教师分配角色...")
                teacher_roles_url = f"{base_url}/teacher_roles/batch_assign/"
                assign_data = {
                    "teacher_ids": [teacher_id],
                    "role_ids": [role_id]
                }
                response = requests.post(teacher_roles_url, json=assign_data, headers=admin_headers)
                response_data = response.json()
                
                if response.status_code == 201:
                    print(f"   ✅ 角色分配成功，创建了 {response_data['created_count']} 个角色关联")
                else:
                    print(f"   ❌ 角色分配失败: {response_data}")
        else:
            print(f"   ❌ 角色创建失败: {response_data}")
    except Exception as e:
        print(f"   ❌ 角色管理过程发生错误: {str(e)}")
else:
    print("\n6. 角色管理功能测试跳过（管理员未登录）")

print("\n===== 教师模块认证集成测试结束 =====")