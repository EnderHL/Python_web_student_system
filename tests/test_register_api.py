import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000/api/auth"

def test_register():
    """测试用户注册功能"""
    # 注册数据
    register_data = {
        "username": "testuser_new_1",
        "email": "testuser_new_1@example.com",
        "password": "testpassword123",
        "password2": "testpassword123",
        "user_type": "student",
        "first_name": "Test",
        "last_name": "User"
    }
    
    print("测试用户注册...")
    print(f"请求数据: {register_data}")
    
    # 发送注册请求
    response = requests.post(f"{BASE_URL}/register/", json=register_data)
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    
    if response.status_code == 201:
        print("注册成功！")
        # 如果注册成功，尝试登录
        login_data = {
            "username": "testuser_new",
            "password": "testpassword123"
        }
        
        print("\n测试用户登录...")
        login_response = requests.post(f"{BASE_URL}/login/", json=login_data)
        
        print(f"登录响应状态码: {login_response.status_code}")
        print(f"登录响应内容: {login_response.text}")
        
        if login_response.status_code == 200:
            print("登录成功！")
            # 获取访问令牌
            tokens = login_response.json().get('tokens')
            if tokens:
                access_token = tokens.get('access')
                print(f"成功获取访问令牌: {access_token[:20]}...")
                
                # 使用令牌访问受保护的资源
                headers = {
                    "Authorization": f"Bearer {access_token}"
                }
                
                profile_response = requests.get(f"{BASE_URL}/profile/", headers=headers)
                print(f"获取个人资料响应状态码: {profile_response.status_code}")
                print(f"获取个人资料响应内容: {profile_response.text}")
    else:
        print("注册失败！")

if __name__ == "__main__":
    test_register()