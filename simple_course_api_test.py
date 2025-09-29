# -*- coding: utf-8 -*-
"""
简单的课程API测试脚本
用于验证登录和获取课程数据的基本功能
"""

import requests
import json
from datetime import datetime

# 配置
BASE_URL = "http://127.0.0.1:8000"
API_ENDPOINTS = {
    'login': f"{BASE_URL}/api/auth/login/",
    'courses': f"{BASE_URL}/api/courses/"
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

# 主测试函数
def main():
    log("===== 简单课程API测试工具 =====", 'header')
    
    # 测试登录
    token = None
    try:
        log("开始测试登录API...")
        login_data = {
            'username': 'root',
            'password': 'root123456'
        }
        login_response = requests.post(API_ENDPOINTS['login'], json=login_data, timeout=10)
        
        log(f"登录请求状态码: {login_response.status_code}")
        
        if login_response.status_code == 200:
            login_data = login_response.json()
            token = login_data.get('tokens', {}).get('access')
            user_data = login_data.get('user', {})
            
            if token:
                log(f"登录成功，获取到token: {token[:20]}...", 'success')
                log(f"登录用户: {user_data.get('username', '')} ({user_data.get('user_type', '')})")
            else:
                log("登录成功，但未获取到token", 'warning')
                print(f"登录响应数据: {json.dumps(login_data, ensure_ascii=False, indent=2)}")
        else:
            log(f"登录失败: {login_response.status_code}", 'error')
            log(f"错误信息: {login_response.text}")
    except Exception as e:
        log(f"登录过程出错: {str(e)}", 'error')
    
    # 测试获取课程列表
    if token:
        try:
            log("\n开始测试获取课程列表API...")
            headers = {'Authorization': f'Bearer {token}'}
            courses_response = requests.get(API_ENDPOINTS['courses'], headers=headers, timeout=10)
            
            log(f"课程列表请求状态码: {courses_response.status_code}")
            
            if courses_response.status_code == 200:
                courses_data = courses_response.json()
                
                # 检查是否是分页数据
                if isinstance(courses_data, dict) and 'results' in courses_data:
                    total_count = courses_data.get('count', 0)
                    current_page_count = len(courses_data.get('results', []))
                    log(f"获取成功！共 {total_count} 门课程，当前页 {current_page_count} 门课程", 'success')
                    
                    # 显示前3门课程
                    if courses_data.get('results'):
                        log("前3门课程:")
                        for i, course in enumerate(courses_data['results'][:3]):
                            log(f"  {i+1}. {course.get('name', '无名称')} (ID: {course.get('id')}, 类型: {course.get('course_type')})")
                elif isinstance(courses_data, list):
                    log(f"获取成功！共 {len(courses_data)} 门课程", 'success')
                    
                    # 显示前3门课程
                    if courses_data:
                        log("前3门课程:")
                        for i, course in enumerate(courses_data[:3]):
                            log(f"  {i+1}. {course.get('name', '无名称')} (ID: {course.get('id')}, 类型: {course.get('course_type')})")
                else:
                    log(f"返回数据格式异常: {type(courses_data)}", 'warning')
            else:
                log(f"获取课程列表失败: {courses_response.status_code}", 'error')
                log(f"错误信息: {courses_response.text}")
        except Exception as e:
            log(f"获取课程列表过程出错: {str(e)}", 'error')
    
    log("\n===== 测试完成 =====", 'header')

if __name__ == '__main__':
    main()