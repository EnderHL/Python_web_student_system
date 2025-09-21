from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserLogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView as SimpleJWTTokenRefreshView

# 创建DefaultRouter实例，用于自动生成API根视图
router = DefaultRouter()

# 手动添加各个端点，因为这些不是标准的ViewSet
urlpatterns = router.urls + [
    # 注册API
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
    # 登录API
    path('login/', UserLoginView.as_view(), name='user-login'),
    
    # JWT Token获取和刷新
    path('token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', SimpleJWTTokenRefreshView.as_view(), name='token-refresh'),
    
    # 用户个人资料
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # 登出API
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
]