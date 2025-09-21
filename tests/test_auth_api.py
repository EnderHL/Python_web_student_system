import requests
import json
import time
import requests

# API基础URL
BASE_URL = "http://127.0.0.1:8000/api/auth"

# 生成唯一的测试用户名，避免重复
current_time = int(time.time())
unique_username = f"testuser_{current_time}"
unique_email = f"testuser_{current_time}@example.com"

# 测试用的用户数据
TEST_USER_DATA = {
    "username": unique_username,
    "email": unique_email,
    "password": "TestPassword123!",
    "password2": "TestPassword123!",  # 确认密码字段名应该是password2
    "user_type": "student",
    "first_name": "Test",  # 必需的名字字段
    "last_name": "User"  # 必需的姓氏字段
}

# 创建一个会话对象，用于保持会话状态
session = requests.Session()

def print_separator():
    """打印分隔符，使输出更清晰"""
    print("=" * 60)

def test_registration():
    """测试用户注册功能"""
    print_separator()
    print("测试用户注册功能")
    print_separator()
    
    url = f"{BASE_URL}/register/"
    response = session.post(url, json=TEST_USER_DATA)
    
    print(f"注册请求URL: {url}")
    print(f"注册请求数据: {TEST_USER_DATA}")
    print(f"注册响应状态码: {response.status_code}")
    try:
        print(f"注册响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except json.JSONDecodeError:
        print(f"注册响应数据: {response.text}")
    
    if response.status_code == 201:
        print("✅ 用户注册成功")
    else:
        print("❌ 用户注册失败")
    
    return response.status_code == 201

def test_login():
    """测试用户登录功能并获取JWT令牌"""
    print_separator()
    print("测试用户登录功能")
    print_separator()
    
    url = f"{BASE_URL}/login/"
    login_data = {
        "username": TEST_USER_DATA["username"],
        "password": TEST_USER_DATA["password"]
    }
    response = session.post(url, json=login_data)
    
    print(f"登录请求URL: {url}")
    print(f"登录请求数据: {login_data}")
    print(f"登录响应状态码: {response.status_code}")
    
    tokens = None
    try:
        response_data = response.json()
        print(f"登录响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        
        if "tokens" in response_data and "access" in response_data["tokens"] and "refresh" in response_data["tokens"]:
            tokens = {
                "access": response_data["tokens"]["access"],
                "refresh": response_data["tokens"]["refresh"]
            }
            print("✅ 用户登录成功，获取JWT令牌")
        else:
            print("❌ 用户登录失败，未获取到JWT令牌")
    except json.JSONDecodeError:
        print(f"登录响应数据: {response.text}")
        print("❌ 用户登录失败")
    
    return tokens

def test_get_profile(access_token):
    """测试获取用户个人资料功能"""
    print_separator()
    print("测试获取用户个人资料功能")
    print_separator()
    
    url = f"{BASE_URL}/profile/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = session.get(url, headers=headers)
    
    print(f"获取个人资料请求URL: {url}")
    print(f"Authorization头: {headers}")
    print(f"获取个人资料响应状态码: {response.status_code}")
    
    try:
        print(f"获取个人资料响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except json.JSONDecodeError:
        print(f"获取个人资料响应数据: {response.text}")
    
    if response.status_code == 200:
        print("✅ 获取用户个人资料成功")
    else:
        print("❌ 获取用户个人资料失败")
    
    return response.status_code == 200

def test_refresh_token(refresh_token):
    """测试刷新JWT令牌功能"""
    print_separator()
    print("测试刷新JWT令牌功能")
    print_separator()
    
    url = f"{BASE_URL}/token/refresh/"
    refresh_data = {"refresh": refresh_token}
    response = session.post(url, json=refresh_data)
    
    print(f"刷新令牌请求URL: {url}")
    print(f"刷新令牌请求数据: {refresh_data}")
    print(f"刷新令牌响应状态码: {response.status_code}")
    
    new_access_token = None
    try:
        response_data = response.json()
        print(f"刷新令牌响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
        
        if "access" in response_data:
            new_access_token = response_data["access"]
            print("✅ 刷新JWT令牌成功")
        else:
            print("❌ 刷新JWT令牌失败")
    except json.JSONDecodeError:
        print(f"刷新令牌响应数据: {response.text}")
        print("❌ 刷新JWT令牌失败")
    
    return new_access_token

def test_logout(tokens):
    """测试用户注销功能"""
    print_separator()
    print("测试用户注销功能")
    print_separator()
    
    url = f"{BASE_URL}/logout/"
    headers = {"Authorization": f"Bearer {tokens['access']}"}
    logout_data = {'refresh': tokens['refresh']}  # 添加刷新令牌到请求体
    response = session.post(url, headers=headers, json=logout_data)
    
    print(f"注销请求URL: {url}")
    print(f"Authorization头: {headers}")
    print(f"注销请求数据: {logout_data}")
    print(f"注销响应状态码: {response.status_code}")
    
    try:
        print(f"注销响应数据: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except json.JSONDecodeError:
        print(f"注销响应数据: {response.text}")
    
    if response.status_code == 200:
        print("✅ 用户注销成功")
    else:
        print("❌ 用户注销失败")
    
    return response.status_code == 200

def main():
    """主函数，按顺序执行所有测试"""
    print("开始测试认证模块功能...")
    
    # 1. 测试用户注册
    registration_success = test_registration()
    if not registration_success:
        print("用户注册失败，无法继续后续测试")
        return
    
    # 等待一会儿，确保用户数据已写入数据库
    time.sleep(1)
    
    # 2. 测试用户登录并获取令牌
    tokens = test_login()
    if not tokens:
        print("用户登录失败，无法继续后续测试")
        return
    
    # 3. 测试获取用户个人资料
    profile_success = test_get_profile(tokens["access"])
    
    # 4. 测试刷新令牌
    new_access_token = test_refresh_token(tokens["refresh"])
    if new_access_token:
        # 使用新令牌再次测试获取个人资料
        print_separator()
        print("使用新刷新的令牌测试获取个人资料")
        test_get_profile(new_access_token)
    
    # 5. 测试用户登出
    logout_success = test_logout(tokens)
    
    # 注意：由于JWT的特性，一旦签发的令牌在过期前都是有效的
    # 我们的登出功能只是验证了令牌的有效性，而没有真正使令牌失效
    # 这是当前配置下的预期行为（未启用黑名单功能）
    print_separator()
    print("注意：由于JWT的特性，登出后令牌在过期前仍有效")
    print("当前配置未启用黑名单功能，这是预期行为")
    
    print_separator()
    print("认证模块功能测试完成")
    print_separator()

if __name__ == "__main__":
    main()