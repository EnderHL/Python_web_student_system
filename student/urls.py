"""
学生应用的URL路由配置
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

# 创建DefaultRouter实例，用于自动生成视图集的URL路由
router = DefaultRouter()

# 注册StudentViewSet到路由中
# prefix: 'students' - URL路径前缀
# viewset: StudentViewSet - 处理请求的视图集
router.register(r'students', StudentViewSet)

# 将生成的URL路由添加到urlpatterns中
# DefaultRouter会自动生成以下路由：
# - GET /api/students/ - 获取学生列表
# - POST /api/students/ - 创建新学生
# - GET /api/students/{id}/ - 获取单个学生详情
# - PUT /api/students/{id}/ - 更新学生信息
# - DELETE /api/students/{id}/ - 删除学生
urlpatterns = router.urls
