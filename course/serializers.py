"""
课程应用的序列化器定义
根据课程表修复方案文档实现
用于处理课程、选课、授课等数据的序列化和反序列化
"""


from rest_framework import serializers
from .models import Course, Enrollment, TeachingAssignment, Classroom, Schedule
from student.models import Student
from teacher.models import Teacher
from django.db import transaction
from django.db.models import Q

class ClassroomSerializer(serializers.ModelSerializer):
    """
    教室模型的序列化器
    根据课程表修复方案文档实现教室表字段定义
    """
    class Meta:
        """序列化器的元数据配置"""
        model = Classroom
        fields = ['id', 'name', 'location', 'capacity', 'equipment']
        read_only_fields = ['id']
    
    def validate_capacity(self, value):
        """验证教室容量的有效性"""
        if value <= 0:
            raise serializers.ValidationError('教室容量必须为正数')
        return value
    
    def validate_name(self, value):
        """验证教室名称唯一性"""
        if not value:
            raise serializers.ValidationError('教室名称不能为空')
        
        # 检查教室名称是否已存在
        qs = Classroom.objects.filter(name=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('该教室名称已存在')
        
        return value

class TeachingAssignmentSerializer(serializers.ModelSerializer):
    """教师授课模型的序列化器
    根据课程表修复方案文档实现教师-课程多对多关联
    """
    # 嵌套序列化教师信息
    teacher_name = serializers.ReadOnlyField(source='teacher.name')
    teacher_id = serializers.IntegerField(write_only=True)
    
    # 嵌套序列化课程信息
    course_name = serializers.ReadOnlyField(source='course.name')
    course_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        """序列化器的元数据配置"""
        model = TeachingAssignment
        fields = [
            'id', 'teacher', 'teacher_id', 'teacher_name',
            'course', 'course_id', 'course_name',
            'assign_date', 'teaching_hours'
        ]
        read_only_fields = ['id', 'assign_date']
    
    def validate_teaching_hours(self, value):
        """验证授课课时字段的有效性"""
        if value <= 0:
            raise serializers.ValidationError('授课课时必须为正数')
        return value
    
    def validate(self, data):
        """验证授课数据的有效性
        根据课程表修复方案文档实现教师-课程关联逻辑
        """
        teacher_id = data.get('teacher_id')
        course_id = data.get('course_id')
        
        # 验证教师是否存在
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            raise serializers.ValidationError({
                'teacher_id': '教师不存在'
            })
        
        # 验证课程是否存在
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError({
                'course_id': '课程不存在'
            })
        
        # 验证教师是否已授该课程
        qs = TeachingAssignment.objects.filter(teacher=teacher, course=course)
        if self.instance:
            qs = qs.exclude(id=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('该教师已经被分配到这门课程')
        
        # 将教师和课程对象存入验证数据中
        data['teacher'] = teacher
        data['course'] = course
        
        return data

class EnrollmentSerializer(serializers.ModelSerializer):
    """学生选课模型的序列化器
    根据课程表修复方案文档实现选课逻辑
    """
    # 嵌套序列化学生信息
    student_name = serializers.ReadOnlyField(source='student.name')
    student_id = serializers.ReadOnlyField(source='student.student_id')
    student_pk = serializers.IntegerField(write_only=True, source='student')
    
    # 嵌套序列化课程信息
    course_name = serializers.ReadOnlyField(source='course.name')
    course_code = serializers.ReadOnlyField(source='course.code')
    course_pk = serializers.IntegerField(write_only=True, source='course')
    
    class Meta:
        """序列化器的元数据配置"""
        model = Enrollment
        fields = [
            'id', 'student', 'student_pk', 'student_name', 'student_id',
            'course', 'course_pk', 'course_name', 'course_code',
            'enroll_date', 'score'
        ]
        read_only_fields = ['id', 'enroll_date']
    
    def validate_score(self, value):
        """验证成绩字段的有效性"""
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError('成绩必须在0-100之间')
        return value
    
    @transaction.atomic
    def validate(self, data):
        """验证选课数据的有效性
        根据课程表修复方案文档实现并发控制和人数校验
        """
        student_pk = data.get('student')
        course_pk = data.get('course')
        
        # 验证学生是否存在
        try:
            student = Student.objects.get(id=student_pk)
        except Student.DoesNotExist:
            raise serializers.ValidationError({
                'student_pk': '学生不存在'
            })
        
        # 验证课程是否存在并加锁（悲观锁）
        try:
            course = Course.objects.select_for_update().get(id=course_pk)
        except Course.DoesNotExist:
            raise serializers.ValidationError({
                'course_pk': '课程不存在'
            })
        
        # 验证学生是否已选该课程
        qs = Enrollment.objects.filter(student=student, course=course)
        if self.instance:
            qs = qs.exclude(id=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('该学生已经选过此课程')
        
        # 验证课程是否已满
        current_students = Enrollment.objects.filter(course=course).count()
        if current_students >= course.max_students:
            raise serializers.ValidationError('该课程选课人数已达上限')
        
        # 将学生和课程对象存入验证数据中
        data['student'] = student
        data['course'] = course
        
        return data

class CourseSerializer(serializers.ModelSerializer):
    """课程模型的序列化器
    根据课程表修复方案文档实现课程信息字段定义
    """
    # 添加教师信息字段
    teachers = serializers.SerializerMethodField()
    
    # 添加学生数量字段
    current_students = serializers.SerializerMethodField()
    
    # 教室关联字段
    classroom_name = serializers.ReadOnlyField(source='classroom.name', allow_null=True)
    classroom_id = serializers.IntegerField(write_only=True, allow_null=True)
    
    class Meta:
        """序列化器的元数据配置"""
        model = Course
        # 课程信息字段定义（10个字段）
        fields = [
            'id', 'name', 'code', 'course_type', 'teaching_method', 
            'credits', 'total_hours', 'semester', 
            'classroom', 'classroom_id', 'classroom_name', 
            'max_students', 'current_students', 
            'description', 'teachers', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'teachers', 'current_students']
    
    def validate_code(self, value):
        """验证课程代码字段的有效性"""
        if not value:
            raise serializers.ValidationError('课程代码不能为空')
        
        # 检查课程代码是否已存在
        qs = Course.objects.filter(code=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('该课程代码已存在')
        
        return value
    
    def validate_credits(self, value):
        """验证学分字段的有效性"""
        if value <= 0:
            raise serializers.ValidationError('学分必须为正数')
        return value
    
    def validate_total_hours(self, value):
        """验证总课时字段的有效性"""
        if value <= 0:
            raise serializers.ValidationError('总课时必须为正数')
        return value
    
    def validate(self, data):
        """验证课程数据的有效性
        根据课程表修复方案文档实现教室与课程的绑定逻辑
        """
        # 授课方式与教室关联验证
        teaching_method = data.get('teaching_method', self.instance.teaching_method if self.instance else None)
        classroom_id = data.get('classroom_id')
        
        # 处理更新操作
        if self.instance:
            if 'teaching_method' not in data:
                teaching_method = self.instance.teaching_method
        
        if teaching_method == 'offline' and not classroom_id and (not self.instance or not self.instance.classroom):
            raise serializers.ValidationError({
                'classroom_id': '线下课程必须选择教室'
            })
        
        if teaching_method == 'online' and classroom_id:
            raise serializers.ValidationError({
                'classroom_id': '线上课程不能选择教室'
            })
        
        # 验证教室是否存在
        if classroom_id:
            try:
                classroom = Classroom.objects.get(id=classroom_id)
                data['classroom'] = classroom
            except Classroom.DoesNotExist:
                raise serializers.ValidationError({
                    'classroom_id': '教室不存在'
                })
        elif teaching_method == 'online':
            data['classroom'] = None
        
        return data
    
    def get_teachers(self, obj):
        """获取教授该课程的教师信息"""
        teachers = [ta.teacher for ta in obj.teaching_assignments.all()]
        return [{'id': teacher.id, 'name': teacher.name, 'title': teacher.title} for teacher in teachers]
    
    def get_current_students(self, obj):
        """获取选修该课程的学生数量"""
        return obj.enrollments.count()

class CourseWithDetailsSerializer(CourseSerializer):
    """扩展的课程序列化器，包含更多详细信息"""
    # 包含选课和授课的详细信息
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    teaching_assignments = TeachingAssignmentSerializer(many=True, read_only=True)
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['enrollments', 'teaching_assignments']

class ScheduleSerializer(serializers.ModelSerializer):
    """排课序列化器，用于排课数据的序列化和反序列化"""
    # 添加课程、教室和教师的详细信息，方便前端显示
    course_name = serializers.ReadOnlyField(source='course.name')
    course_code = serializers.ReadOnlyField(source='course.code')
    classroom_name = serializers.ReadOnlyField(source='classroom.name')
    classroom_location = serializers.ReadOnlyField(source='classroom.location')
    teacher_name = serializers.ReadOnlyField(source='teaching_assignment.teacher.name')
    
    class Meta:
        model = Schedule
        fields = ['id', 'course', 'classroom', 'teaching_assignment', 'day_of_week', 
                 'start_section', 'end_section', 'week_pattern', 'course_name', 
                 'course_code', 'classroom_name', 'classroom_location', 'teacher_name']
        read_only_fields = ['id']
    
    def validate_day_of_week(self, value):
        """验证星期几的有效性"""
        if value < 1 or value > 7:
            raise serializers.ValidationError('星期几必须在1-7之间')
        return value
    
    def validate_start_section(self, value):
        """验证开始节次的有效性"""
        if value <= 0:
            raise serializers.ValidationError('开始节次必须为正数')
        return value
    
    def validate_end_section(self, value):
        """验证结束节次的有效性"""
        if value <= 0:
            raise serializers.ValidationError('结束节次必须为正数')
        return value
    
    def validate(self, data):
        """验证排课数据的有效性，实现排课冲突检查"""
        # 验证开始节次小于结束节次
        if data.get('start_section') and data.get('end_section'):
            if data['start_section'] >= data['end_section']:
                raise serializers.ValidationError('开始节次必须小于结束节次')
        
        # 验证排课冲突
        course_id = data.get('course')
        classroom_id = data.get('classroom')
        teaching_assignment_id = data.get('teaching_assignment')
        day_of_week = data.get('day_of_week')
        start_section = data.get('start_section')
        end_section = data.get('end_section')
        week_pattern = data.get('week_pattern')
        
        # 检查教室排课冲突
        if classroom_id and day_of_week and start_section and end_section and week_pattern:
            # 构建查询条件
            query = Q(classroom=classroom_id) & Q(day_of_week=day_of_week) & Q(week_pattern=week_pattern)
            
            # 排除当前实例（更新操作）
            if self.instance:
                query = query & ~Q(id=self.instance.id)
            
            # 检查时间重叠
            time_query = (
                Q(start_section__lte=start_section) & Q(end_section__gte=start_section) |
                Q(start_section__lte=end_section) & Q(end_section__gte=end_section) |
                Q(start_section__gte=start_section) & Q(end_section__lte=end_section)
            )
            
            if Schedule.objects.filter(query & time_query).exists():
                raise serializers.ValidationError('该教室在该时间段已有排课')
        
        # 检查教师排课冲突
        if teaching_assignment_id and day_of_week and start_section and end_section and week_pattern:
            # 构建查询条件
            query = Q(teaching_assignment=teaching_assignment_id) & Q(day_of_week=day_of_week) & Q(week_pattern=week_pattern)
            
            # 排除当前实例（更新操作）
            if self.instance:
                query = query & ~Q(id=self.instance.id)
            
            # 检查时间重叠
            time_query = (
                Q(start_section__lte=start_section) & Q(end_section__gte=start_section) |
                Q(start_section__lte=end_section) & Q(end_section__gte=end_section) |
                Q(start_section__gte=start_section) & Q(end_section__lte=end_section)
            )
            
            if Schedule.objects.filter(query & time_query).exists():
                raise serializers.ValidationError('该教师在该时间段已有排课')
        
        return data