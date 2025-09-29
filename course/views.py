from django.shortcuts import render

"""
课程应用的视图定义
根据课程表修复方案文档实现
处理课程相关的API请求
"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import IntegrityError, transaction
from django.db.models import Q

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
    """课程视图集
    根据课程表修复方案文档实现课程信息管理的完整CRUD操作
    支持课程列表、详情、创建、更新和删除功能
    """
    # 查询集：获取所有课程数据
    queryset = Course.objects.all()
    # 默认序列化器
    serializer_class = CourseSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """根据请求操作选择合适的序列化器
        详情操作时使用包含更多信息的序列化器
        """
        if self.action == 'retrieve':
            return CourseWithDetailsSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        """创建课程前的处理逻辑
        根据课程表修复方案文档实现教室与课程的绑定逻辑
        """
        # 获取课程数据
        course_data = serializer.validated_data
        
        # 处理线上课程的特殊逻辑
        if course_data.get('teaching_method') == 'online':
            # 线上课程容量固定为1000人
            course_data['max_students'] = 1000
            # 线上课程清空教室关联
            course_data['classroom'] = None
        elif course_data.get('teaching_method') == 'offline' and 'classroom' in course_data:
            # 线下课程使用教室容量
            course_data['max_students'] = course_data['classroom'].capacity
        
        # 保存课程
        super().perform_create(serializer)
    
    def create(self, request, *args, **kwargs):
        """重写create方法，添加数据库事务和唯一性错误处理
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
    
    def perform_update(self, serializer):
        """更新课程前的处理逻辑
        根据课程表修复方案文档实现教室与课程的绑定逻辑
        """
        # 获取课程数据
        course_data = serializer.validated_data
        
        # 处理线上课程的特殊逻辑
        if course_data.get('teaching_method') == 'online':
            # 线上课程容量固定为1000人
            course_data['max_students'] = 1000
            # 线上课程清空教室关联
            course_data['classroom'] = None
        elif course_data.get('teaching_method') == 'offline' and 'classroom' in course_data:
            # 线下课程使用教室容量
            course_data['max_students'] = course_data['classroom'].capacity
        
        # 保存课程
        super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        """重写删除方法，确保在删除课程前先删除相关的选课和授课记录
        维护数据的完整性
        """
        # 先删除相关的选课记录
        instance.enrollments.all().delete()
        # 再删除相关的授课记录
        instance.teaching_assignments.all().delete()
        # 最后删除课程本身
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def current_status(self, request, pk=None):
        """获取课程当前状态信息
        返回课程的已选人数、剩余名额等信息
        """
        course = self.get_object()
        current_students = course.enrollments.count()
        available_slots = max(0, course.max_students - current_students)
        
        return Response({
            'course_id': course.id,
            'course_name': course.name,
            'current_students': current_students,
            'max_students': course.max_students,
            'available_slots': available_slots,
            'is_full': current_students >= course.max_students
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """高级搜索课程
        支持按名称、代码、类型、学期等多条件搜索
        """
        queryset = self.get_queryset()
        
        # 获取搜索参数
        name = request.query_params.get('name')
        code = request.query_params.get('code')
        course_type = request.query_params.get('course_type')
        semester = request.query_params.get('semester')
        teaching_method = request.query_params.get('teaching_method')
        min_credits = request.query_params.get('min_credits')
        max_credits = request.query_params.get('max_credits')
        
        # 构建查询条件
        if name:
            queryset = queryset.filter(name__icontains=name)
        if code:
            queryset = queryset.filter(code__icontains=code)
        if course_type:
            queryset = queryset.filter(course_type=course_type)
        if semester:
            queryset = queryset.filter(semester=semester)
        if teaching_method:
            queryset = queryset.filter(teaching_method=teaching_method)
        if min_credits:
            queryset = queryset.filter(credits__gte=float(min_credits))
        if max_credits:
            queryset = queryset.filter(credits__lte=float(max_credits))
        
        # 序列化数据
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class EnrollmentViewSet(viewsets.ModelViewSet):
    """选课视图集
    根据课程表修复方案文档实现学生选课的完整CRUD操作
    支持选课记录的创建、查询、更新和删除
    """
    # 查询集：获取所有选课记录
    queryset = Enrollment.objects.all()
    # 序列化器
    serializer_class = EnrollmentSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """根据请求参数过滤查询集
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
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """重写create方法，使用事务确保选课操作的原子性
        根据课程表修复方案文档实现并发控制和人数校验
        """
        # 获取序列化器并验证数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 提取学生和课程对象
        student = serializer.validated_data.get('student')
        course = serializer.validated_data.get('course')
        
        try:
            # 锁定课程记录，避免并发修改（悲观锁）
            course = Course.objects.select_for_update().get(id=course.id)
            
            # 再次检查课程人数是否已满（双重检查）
            current_students = Enrollment.objects.filter(course=course).count()
            if current_students >= course.max_students:
                return Response(
                    {"error": "该课程选课人数已达上限"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 检查学生是否已经选过该课程
            if Enrollment.objects.filter(student=student, course=course).exists():
                return Response(
                    {"error": "该学生已经选过此课程"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 创建选课记录
            self.perform_create(serializer)
        except Course.DoesNotExist:
            return Response(
                {"error": "课程不存在"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class ClassroomViewSet(viewsets.ModelViewSet):
    """教室视图集
    根据课程表修复方案文档实现教室管理的完整CRUD操作
    支持教室的创建、查询、更新和删除
    """
    # 查询集：获取所有教室数据
    queryset = Classroom.objects.all()
    # 序列化器
    serializer_class = ClassroomSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """获取当前可用的教室列表
        返回未被占用或即将可用的教室
        """
        # 这里可以实现更复杂的可用教室查询逻辑
        # 目前返回所有教室
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ScheduleViewSet(viewsets.ModelViewSet):
    """排课视图集
    根据课程表修复方案文档实现排课管理的完整CRUD操作
    支持排课记录的创建、查询、更新和删除
    """
    # 查询集：获取所有排课记录
    queryset = Schedule.objects.all()
    # 序列化器
    serializer_class = ScheduleSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """根据请求参数过滤查询集
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
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """重写create方法，添加排课冲突检查和课程容量设置
        根据课程表修复方案文档实现教室与课程的绑定逻辑
        """
        # 获取序列化器并验证数据
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 提取数据进行冲突检查
        course = serializer.validated_data.get('course')
        classroom = serializer.validated_data.get('classroom')
        teaching_assignment = serializer.validated_data.get('teaching_assignment')
        day_of_week = serializer.validated_data.get('day_of_week')
        start_section = serializer.validated_data.get('start_section')
        end_section = serializer.validated_data.get('end_section')
        week_pattern = serializer.validated_data.get('week_pattern')
        
        # 检查课程是否为线上课程，如果是则不允许分配教室
        if course.teaching_method == 'online':
            return Response(
                {"error": "线上课程不允许分配教室"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查课程是否为线下课程，如果是则必须分配教室
        if course.teaching_method == 'offline' and not classroom:
            return Response(
                {"error": "线下课程必须分配教室"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 检查教室排课冲突
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
        
        # 检查教师排课冲突
        conflicting_teacher_schedules = Schedule.objects.filter(
            teaching_assignment=teaching_assignment,
            day_of_week=day_of_week,
            week_pattern=week_pattern
        ).exclude(
            # 排除时间上不重叠的排课
            end_section__lte=start_section
        ).exclude(
            start_section__gte=end_section
        )
        
        if conflicting_teacher_schedules.exists():
            return Response(
                {"error": "该教师在指定时间已有排课"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 使用事务确保数据一致性
        with transaction.atomic():
            # 如果是线下课程，自动设置课程容量为教室容量
            if course.teaching_method == 'offline' and classroom:
                course.max_students = classroom.capacity
                course.classroom = classroom  # 关联课程和教室
                course.save()
            
            # 创建排课记录
            self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class TeachingAssignmentViewSet(viewsets.ModelViewSet):
    """授课视图集
    根据课程表修复方案文档实现教师-课程多对多关联
    支持授课记录的创建、查询、更新和删除
    """
    # 查询集：获取所有授课记录
    queryset = TeachingAssignment.objects.all()
    # 序列化器
    serializer_class = TeachingAssignmentSerializer
    # 权限控制：要求用户必须登录
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """根据请求参数过滤查询集
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
