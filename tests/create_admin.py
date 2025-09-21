import sys
import os

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

# 导入用户模型
from user_auth.models import CustomUser
from django.contrib.auth.hashers import make_password

# 检查是否已存在root用户
try:
    root_user = CustomUser.objects.get(username='root')
    print("root超级管理员用户已存在，无需创建")
    print(f"用户名: {root_user.username}")
    print(f"用户类型: {root_user.user_type}")
    print(f"是超级用户: {root_user.is_superuser}")
    print(f"是活跃用户: {root_user.is_active}")
except CustomUser.DoesNotExist:
    # 创建root超级管理员用户
    root_user = CustomUser.objects.create(
        username='root',
        email='root@example.com',
        password=make_password('root123456'),
        first_name='系统',
        last_name='超级管理员',
        user_type='admin',
        is_active=True,
        is_staff=True,
        is_superuser=True
    )
    
    print("✅ root超级管理员用户创建成功!")
    print(f"用户名: {root_user.username}")
    print(f"密码: root123456")
    print(f"用户类型: {root_user.user_type}")
    print(f"是超级用户: {root_user.is_superuser}")
    print(f"是活跃用户: {root_user.is_active}")