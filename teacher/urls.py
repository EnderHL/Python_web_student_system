"""
教师应用的URL配置模块
定义教师管理API的路由规则
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet
from .role_views import RoleViewSet, TeacherRoleViewSet

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'teacher_roles', TeacherRoleViewSet)

# 定义URL模式列表
urlpatterns = [
    # 包含路由器生成的所有URL
    path('', include(router.urls)),
]