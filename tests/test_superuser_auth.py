import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')
import django
django.setup()
from django.contrib.auth import authenticate
from user_auth.models import CustomUser

# 尝试获取root用户
print("=== 测试超级用户认证 ===")
try:
    user = CustomUser.objects.get(username='root')
    print(f"找到用户: {user.username}")
    print(f"用户类型: {user.user_type}")
    print(f"是否是超级用户: {user.is_superuser}")
    print(f"是否活跃: {user.is_active}")
    print(f"密码哈希: {user.password}")
    
    # 测试认证
    print("\n测试认证过程:")
    # 尝试使用默认密码 'root123456' 进行认证
    authenticated_user = authenticate(username='root', password='root123456')
    
    if authenticated_user:
        print("✅ 认证成功!")
        print(f"认证后的用户: {authenticated_user.username}")
        print(f"认证后的用户类型: {authenticated_user.user_type}")
        print(f"认证后的超级用户状态: {authenticated_user.is_superuser}")
    else:
        print("❌ 认证失败! 用户名或密码错误。")
        
        # 尝试重置密码为 'root123456'
        print("\n尝试重置root用户密码为 'root123456'...")
        user.set_password('root123456')
        user.save()
        print("密码已重置。")
        
        # 再次尝试认证
        new_authenticated_user = authenticate(username='root', password='root123456')
        if new_authenticated_user:
            print("✅ 重置密码后认证成功!")
        else:
            print("❌ 重置密码后仍认证失败!")
            
except CustomUser.DoesNotExist:
    print("❌ 未找到root用户!")
    
print("\n=== 测试完成 ===")