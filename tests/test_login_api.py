import os
import requests
import json

# API基础URL
BASE_URL = 'http://127.0.0.1:8000/api/auth/'

# 测试root用户登录
def test_root_login():
    print("=== 测试root用户登录API ===")
    
    # 登录请求数据
    login_data = {
        'username': 'root',
        'password': 'root123456'
    }
    
    # 发送登录请求
    try:
        response = requests.post(
            f'{BASE_URL}login/',
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ API登录测试成功！")
            data = response.json()
            print(f"返回的用户信息: {data.get('user', {})}")
            print(f"是否包含token: {'tokens' in data}")
        else:
            print("❌ API登录测试失败！")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        print("请确保Django服务器正在运行！")

def main():
    test_root_login()
    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    main()