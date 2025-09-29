#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
课程数据和API测试脚本
用于诊断课程管理页面无法查询到数据的后端问题
"""

import os
import sys
import requests
import json
from datetime import datetime

# 设置脚本路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base_dir)

# 设置Django环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')

# 尝试导入Django设置，用于直接数据库操作
try:
    import django
    django.setup()
    from course.models import Course, Classroom, Teacher
    from user_auth.models import CustomUser
    HAS_DJANGO = True
    print("✅ 成功导入Django设置和模型")
except ImportError:
    HAS_DJANGO = False
    print("⚠️ 无法导入Django设置，将只进行API测试")

# 配置
BASE_URL = "http://127.0.0.1:8000"
API_ENDPOINTS = {
    'courses': f"{BASE_URL}/api/courses/",
    'login': f"{BASE_URL}/api/auth/login/",
    'user': f"{BASE_URL}/api/user/"
}

# 颜色输出
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 日志函数
def log(message, level='info'):
    """输出带时间戳和颜色的日志"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    if level == 'info':
        print(f"{Colors.OKBLUE}[{timestamp}] {message}{Colors.ENDC}")
    elif level == 'success':
        print(f"{Colors.OKGREEN}[{timestamp}] {message}{Colors.ENDC}")
    elif level == 'warning':
        print(f"{Colors.WARNING}[{timestamp}] {message}{Colors.ENDC}")
    elif level == 'error':
        print(f"{Colors.FAIL}[{timestamp}] {message}{Colors.ENDC}")
    elif level == 'header':
        print(f"\n{Colors.HEADER}{Colors.BOLD}{message}{Colors.ENDC}\n")

# 数据库检查函数
def check_database():
    """直接检查数据库中的课程相关数据"""
    if not HAS_DJANGO:
        log("无法直接检查数据库，跳过此步骤", 'warning')
        return
    
    log("=== 开始数据库检查 ===", 'header')
    
    # 检查课程数据
    try:
        total_courses = Course.objects.count()
        log(f"课程总数: {total_courses}", 'info')
        
        if total_courses > 0:
            # 获取前5门课程的基本信息
            recent_courses = Course.objects.all()[:5]
            log("最近的5门课程:", 'info')
            for course in recent_courses:
                status = "已满" if course.current_students >= course.max_students else "可报名"
                log(f"  - {course.name} (代码: {course.code}, 学分: {course.credits}, 状态: {status})")
        else:
            log("数据库中没有课程数据，请先添加课程", 'warning')
    except Exception as e:
        log(f"检查课程数据时出错: {str(e)}", 'error')
    
    # 检查教师数据
    try:
        total_teachers = Teacher.objects.count()
        log(f"教师总数: {total_teachers}", 'info')
        if total_teachers == 0:
            log("数据库中没有教师数据，这可能导致无法创建课程", 'warning')
    except Exception as e:
        log(f"检查教师数据时出错: {str(e)}", 'error')
    
    # 检查教室数据
    try:
        total_classrooms = Classroom.objects.count()
        log(f"教室总数: {total_classrooms}", 'info')
        if total_classrooms == 0:
            log("数据库中没有教室数据，这可能导致无法创建线下课程", 'warning')
    except Exception as e:
        log(f"检查教室数据时出错: {str(e)}", 'error')
    
    # 检查用户数据
    try:
        total_users = CustomUser.objects.count()
        admin_users = CustomUser.objects.filter(is_superuser=True).count()
        log(f"用户总数: {total_users}, 管理员用户数: {admin_users}", 'info')
    except Exception as e:
        log(f"检查用户数据时出错: {str(e)}", 'error')
    
    log("=== 数据库检查完成 ===", 'header')

# API测试函数
def test_api():
    """测试课程相关的API端点"""
    log("=== 开始API测试 ===", 'header')
    
    # 检查服务器连接
    try:
        response = requests.head(BASE_URL, timeout=5)
        log(f"服务器连接成功，状态码: {response.status_code}", 'success')
    except requests.exceptions.RequestException as e:
        log(f"服务器连接失败: {str(e)}", 'error')
        log("请确认Django服务器是否正在运行: python manage.py runserver", 'warning')
        return None
    
    # 尝试登录（如果有提供凭据）
    token = None
    try:
        # 尝试使用默认的admin账号登录
        login_data = {
            'username': 'root',
            'password': 'root123456'
        }
        login_response = requests.post(API_ENDPOINTS['login'], json=login_data)
        
        if login_response.status_code == 200:
            token = login_response.json().get('tokens', {}).get('access')
            log("使用root账号登录成功", 'success')
        else:
            log(f"登录失败: {login_response.status_code} - {login_response.text}", 'warning')
            log("将尝试匿名访问API", 'info')
    except Exception as e:
        log(f"登录过程出错: {str(e)}", 'error')
    
    # 设置请求头
    headers = {}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    # 测试获取课程列表API
    try:
        # 1. 测试无参数请求
        log("测试1: 获取所有课程（无参数）", 'info')
        response = requests.get(API_ENDPOINTS['courses'], headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            log(f"请求成功，状态码: {response.status_code}", 'success')
            log(f"响应数据类型: {type(data)}", 'info')
            
            # 检查是否是分页数据
            if isinstance(data, dict) and 'results' in data:
                log(f"分页数据 - 总条数: {data.get('count', 0)}")
                log(f"分页数据 - 当前页课程数量: {len(data.get('results', []))}")
                if data.get('results'):
                    log("前3条课程数据:")
                    for i, course in enumerate(data['results'][:3]):
                        log(f"  {i+1}. {course.get('name', '无名称')} (ID: {course.get('id')})")
            elif isinstance(data, list):
                log(f"返回课程数量: {len(data)}")
                if data:
                    log("前3条课程数据:")
                    for i, course in enumerate(data[:3]):
                        log(f"  {i+1}. {course.get('name', '无名称')} (ID: {course.get('id')})")
            else:
                log(f"返回数据格式异常: {type(data)}", 'warning')
                log(f"数据示例: {json.dumps(data, ensure_ascii=False, indent=2)[:200]}...")
        else:
            log(f"请求失败: {response.status_code} - {response.text}", 'error')
            
            # 常见错误处理
            if response.status_code == 401:
                log("认证失败，请确认是否已登录或token是否有效", 'warning')
            elif response.status_code == 403:
                log("权限不足，当前用户可能没有访问课程数据的权限", 'warning')
            elif response.status_code == 404:
                log("API端点不存在，请检查URL是否正确", 'warning')
    except Exception as e:
        log(f"获取课程列表时出错: {str(e)}", 'error')
    
    # 测试带参数的请求
    try:
        log("\n测试2: 获取必修课程（带参数）", 'info')
        params = {'course_type': '必修'}
        response = requests.get(API_ENDPOINTS['courses'], params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            result_count = len(data) if isinstance(data, list) else data.get('count', 0) if isinstance(data, dict) else 0
            log(f"请求成功，找到 {result_count} 门必修课程", 'success')
        else:
            log(f"请求失败: {response.status_code} - {response.text}", 'error')
    except Exception as e:
        log(f"获取必修课程时出错: {str(e)}", 'error')
    
    # 检查当前用户信息
    if token:
        try:
            log("\n测试3: 检查当前用户信息", 'info')
            response = requests.get(API_ENDPOINTS['user'], headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                log(f"用户信息获取成功", 'success')
                log(f"用户名: {user_data.get('username')}")
                log(f"用户角色: {user_data.get('role', '未知')}")
                log(f"是否是管理员: {user_data.get('is_superuser', False)}")
            else:
                log(f"获取用户信息失败: {response.status_code} - {response.text}", 'error')
        except Exception as e:
            log(f"获取用户信息时出错: {str(e)}", 'error')
    
    log("=== API测试完成 ===", 'header')
    return token

# 生成诊断报告
def generate_diagnostic_report(token):
    """生成问题诊断报告"""
    log("=== 问题诊断报告 ===", 'header')
    
    issues = []
    
    # 检查服务器连接
    try:
        requests.head(BASE_URL, timeout=5)
    except:
        issues.append("❌ 后端服务器未运行或无法访问")
    
    # 检查认证状态
    if not token:
        issues.append("⚠️ 未成功登录，可能导致访问受限")
    
    # 检查数据库数据（如果有Django）
    if HAS_DJANGO:
        try:
            if Course.objects.count() == 0:
                issues.append("⚠️ 数据库中没有课程数据")
            if Teacher.objects.count() == 0:
                issues.append("⚠️ 数据库中没有教师数据")
        except:
            pass
    
    # 如果没有发现问题
    if not issues:
        log("✅ 未发现明显问题，可能是前端展示逻辑问题", 'success')
    else:
        log("发现以下可能的问题:", 'warning')
        for issue in issues:
            log(issue)
    
    log("\n建议的解决方案:", 'info')
    log("1. 确保Django服务器正在运行: python manage.py runserver")
    log("2. 确保已使用正确的账号登录系统")
    log("3. 如果数据库中没有数据，可以使用Django管理后台添加课程数据")
    log("4. 检查前端代码中的API调用逻辑和数据处理逻辑")
    log("5. 检查浏览器控制台是否有其他错误信息")
    
    log("=== 诊断报告结束 ===", 'header')

# 主函数
def main():
    """主函数"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}===== 课程数据和API测试工具 ====={Colors.ENDC}\n")
    
    # 1. 检查数据库
    check_database()
    
    # 2. 测试API
    token = test_api()
    
    # 3. 生成诊断报告
    generate_diagnostic_report(token)
    
    print(f"\n{Colors.HEADER}测试完成，请查看上述输出以获取诊断信息{Colors.ENDC}")

if __name__ == "__main__":
    main()