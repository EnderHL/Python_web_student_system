import os
import sys

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_web_student_system.settings')

# 初始化Django
try:
    import django
    django.setup()
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc

# 现在可以导入Django模型了
from user_auth.models import CustomUser

# 查询所有用户
users = CustomUser.objects.all()

print(f"用户数量: {users.count()}")
print("\n用户列表:")
print("用户名 | 用户类型 | 是超级用户 | 是活跃用户")
print("-" * 50)
for user in users:
    print(f"{user.username} | {user.user_type} | {user.is_superuser} | {user.is_active}")

# 检查是否存在admin用户
try:
    admin_user = CustomUser.objects.get(username='admin')
    print(f"\nadmin用户存在：")
    print(f"用户名: {admin_user.username}")
    print(f"用户类型: {admin_user.user_type}")
    print(f"是超级用户: {admin_user.is_superuser}")
    print(f"是活跃用户: {admin_user.is_active}")
except CustomUser.DoesNotExist:
    print("\nadmin用户不存在")