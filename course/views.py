from django.shortcuts import render

"""
课程应用的视图定义
处理课程相关的API请求
"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import IntegrityError, transaction

from .models import Course, Enrollment, TeachingAssignment, Classroom, Schedule
from .serializers import (
    CourseSerializer,
    EnrollmentSerializer,
    TeachingAssignmentSerializer,
    CourseWithDetailsSerializer,
    ClassroomSerializer,
    ScheduleSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    """
    课程视图集，提供课程的完整CRUD操作
    - GET /api/courses/ - 获取课程列表
    - POST /api/courses/ - 创建新课程
    - GET /api/courses/{id}/ - 获取单个课程详情
    - PUT /api/courses/{id}/ - 更新课程信息
    - DELETE /api/courses/{id}/ - 删除课程
    """
    # 查询集：获取所有课程数据
    queryset = Course.objects.all()
    # 默认序列化器
    serializer_class = CourseSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """
        根据请求操作选择合适的序列化器
        详情操作时使用包含更多信息的序列化器
        """
        if self.action == 'retrieve':
            return CourseWithDetailsSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        """
        重写create方法，添加数据库事务和唯一性错误处理
        确保在课程代码重复时返回友好的错误信息
        """
        # 获取序列化器并验证数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # 使用事务确保数据一致性
            with transaction.atomic():
                self.perform_create(serializer)
        except IntegrityError:
            # 捕获并处理课程代码唯一性冲突
            return Response(
                {"code": ["该课程代码已存在"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def perform_destroy(self, instance):
        """
        重写删除方法，确保在删除课程前先删除相关的选课和授课记录
        """
        # 先删除相关的选课记录
        instance.enrollments.all().delete()
        # 再删除相关的授课记录
        instance.teaching_assignments.all().delete()
        # 最后删除课程本身
        instance.delete()

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    选课视图集，提供选课记录的完整CRUD操作
    - GET /api/enrollments/ - 获取选课记录列表
    - POST /api/enrollments/ - 创建新的选课记录
    - GET /api/enrollments/{id}/ - 获取单个选课记录详情
    - PUT /api/enrollments/{id}/ - 更新选课记录（如成绩）
    - DELETE /api/enrollments/{id}/ - 删除选课记录
    """
    # 查询集：获取所有选课记录
    queryset = Enrollment.objects.all()
    # 序列化器
    serializer_class = EnrollmentSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        根据请求参数过滤查询集
        支持按学生ID或课程ID过滤
        """
        queryset = super().get_queryset()
        
        # 获取请求中的过滤参数
        student_id = self.request.query_params.get('student_id')
        course_id = self.request.query_params.get('course_id')
        
        # 按学生ID过滤
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        
        # 按课程ID过滤
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        return queryset


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    教室视图集，提供教室的完整CRUD操作
    - GET /api/classrooms/ - 获取教室列表
    - POST /api/classrooms/ - 创建新教室
    - GET /api/classrooms/{id}/ - 获取单个教室详情
    - PUT /api/classrooms/{id}/ - 更新教室信息
    - DELETE /api/classrooms/{id}/ - 删除教室
    """
    # 查询集：获取所有教室数据
    queryset = Classroom.objects.all()
    # 序列化器
    serializer_class = ClassroomSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    排课视图集，提供排课记录的完整CRUD操作
    - GET /api/schedules/ - 获取排课记录列表
    - POST /api/schedules/ - 创建新的排课记录
    - GET /api/schedules/{id}/ - 获取单个排课记录详情
    - PUT /api/schedules/{id}/ - 更新排课记录
    - DELETE /api/schedules/{id}/ - 删除排课记录
    """
    # 查询集：获取所有排课记录
    queryset = Schedule.objects.all()
    # 序列化器
    serializer_class = ScheduleSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        根据请求参数过滤查询集
        支持按课程ID、教室ID、教师ID或星期几过滤
        """
        queryset = super().get_queryset()
        
        # 获取请求中的过滤参数
        course_id = self.request.query_params.get('course_id')
        classroom_id = self.request.query_params.get('classroom_id')
        teaching_assignment_id = self.request.query_params.get('teaching_assignment_id')
        day_of_week = self.request.query_params.get('day_of_week')
        
        # 按课程ID过滤
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        # 按教室ID过滤
        if classroom_id:
            queryset = queryset.filter(classroom_id=classroom_id)
        
        # 按授课记录ID过滤
        if teaching_assignment_id:
            queryset = queryset.filter(teaching_assignment_id=teaching_assignment_id)
        
        # 按星期几过滤
        if day_of_week:
            queryset = queryset.filter(day_of_week=day_of_week)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """
        重写create方法，添加排课冲突检查
        确保在创建排课前检查是否有时间冲突
        """
        # 获取序列化器并验证数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 提取数据进行冲突检查
        classroom = serializer.validated_data.get('classroom')
        day_of_week = serializer.validated_data.get('day_of_week')
        start_section = serializer.validated_data.get('start_section')
        end_section = serializer.validated_data.get('end_section')
        week_pattern = serializer.validated_data.get('week_pattern')
        
        # 检查教室排课冲突
        # 这里简化处理，实际应用中应该考虑更复杂的排课规则
        conflicting_schedules = Schedule.objects.filter(
            classroom=classroom,
            day_of_week=day_of_week,
            week_pattern=week_pattern
        ).exclude(
            # 排除时间上不重叠的排课
            end_section__lte=start_section
        ).exclude(
            start_section__gte=end_section
        )
        
        if conflicting_schedules.exists():
            return Response(
                {"error": "该教室在指定时间已被占用"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 如果没有冲突，创建排课记录
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class TeachingAssignmentViewSet(viewsets.ModelViewSet):
    """
    授课视图集，提供授课记录的完整CRUD操作
    - GET /api/teaching_assignments/ - 获取授课记录列表
    - POST /api/teaching_assignments/ - 创建新的授课记录
    - GET /api/teaching_assignments/{id}/ - 获取单个授课记录详情
    - PUT /api/teaching_assignments/{id}/ - 更新授课记录
    - DELETE /api/teaching_assignments/{id}/ - 删除授课记录
    """
    # 查询集：获取所有授课记录
    queryset = TeachingAssignment.objects.all()
    # 序列化器
    serializer_class = TeachingAssignmentSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        根据请求参数过滤查询集
        支持按教师ID或课程ID过滤
        """
        queryset = super().get_queryset()
        
        # 获取请求中的过滤参数
        teacher_id = self.request.query_params.get('teacher_id')
        course_id = self.request.query_params.get('course_id')
        
        # 按教师ID过滤
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        # 按课程ID过滤
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        
        return queryset
