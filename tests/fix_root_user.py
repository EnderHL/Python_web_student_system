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

# 检查并修复root用户
try:
    root_user = CustomUser.objects.get(username='root')
    print(f"当前root用户信息:")
    print(f"用户名: {root_user.username}")
    print(f"用户类型: {root_user.user_type}")
    print(f"是超级用户: {root_user.is_superuser}")
    print(f"是活跃用户: {root_user.is_active}")
    
    # 如果user_type不是admin，则修改
    if root_user.user_type != 'admin':
        root_user.user_type = 'admin'
        root_user.save()
        print("✅ root用户的user_type已成功修改为admin")
    else:
        print("root用户的user_type已经是admin，无需修改")
        
    # 确保root用户是超级用户和活跃用户
    if not root_user.is_superuser:
        root_user.is_superuser = True
        root_user.save()
        print("✅ root用户已设置为超级用户")
    
    if not root_user.is_active:
        root_user.is_active = True
        root_user.save()
        print("✅ root用户已设置为活跃用户")
        
except CustomUser.DoesNotExist:
    print("❌ root用户不存在，请先运行create_admin.py创建root用户")