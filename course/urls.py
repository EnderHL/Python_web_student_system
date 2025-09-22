"""
课程应用的URL路由配置
定义课程管理相关API的路由规则
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, EnrollmentViewSet, TeachingAssignmentViewSet, ClassroomViewSet, ScheduleViewSet

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'teaching_assignments', TeachingAssignmentViewSet)
router.register(r'classrooms', ClassroomViewSet)
router.register(r'schedules', ScheduleViewSet)

# 定义URL模式列表
urlpatterns = [
    # 包含路由器生成的所有URL
    path('', include(router.urls)),
]