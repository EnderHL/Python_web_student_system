from django.contrib.auth import authenticate
from user_auth.models import CustomUser

print('=== 测试超级用户认证 ===')
try:
    user = CustomUser.objects.get(username='root')
    print(f'找到用户: {user.username}')
    print(f'用户类型: {user.user_type}')
    print(f'是否是超级用户: {user.is_superuser}')
    print(f'是否活跃: {user.is_active}')
    
    # 测试认证
    print('\n测试认证过程:')
    authenticated_user = authenticate(username='root', password='root123456')
    
    if authenticated_user:
        print('✅ 认证成功!')
    else:
        print('❌ 认证失败! 用户名或密码错误。')
        
        # 重置密码
        print('\n尝试重置密码为 "root123456"...')
        user.set_password('root123456')
        user.save()
        print('密码已重置。')
        
        # 再次认证
        new_authenticated_user = authenticate(username='root', password='root123456')
        if new_authenticated_user:
            print('✅ 重置密码后认证成功!')
        else:
            print('❌ 重置密码后仍认证失败!')

except CustomUser.DoesNotExist:
    print('❌ 未找到root用户!')
    
print('\n=== 测试完成 ===')