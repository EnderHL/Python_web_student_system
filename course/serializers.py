"""
课程应用的序列化器定义
负责课程相关数据的序列化和反序列化
"""
from rest_framework import serializers
from .models import Course, Enrollment, TeachingAssignment, Classroom, Schedule
from student.models import Student
from teacher.models import Teacher

class CourseSerializer(serializers.ModelSerializer):
    """
    课程序列化器，用于课程数据的序列化和反序列化
    - 序列化：将课程模型实例转换为JSON格式
    - 反序列化：将JSON数据转换为课程模型实例并进行验证
    """
    # 添加教师信息字段，方便前端显示（可选）
    teachers = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    
    class Meta:
        # 指定使用的模型类
        model = Course
        # 指定序列化的字段列表
        fields = ['id', 'name', 'code', 'credits', 'description', 'total_hours', 'semester', 
                  'created_at', 'updated_at', 'teachers', 'student_count']
        # 指定只读字段
        read_only_fields = ['id', 'created_at', 'updated_at', 'teachers', 'student_count']
    
    def validate_code(self, value):
        """
        验证课程代码字段的有效性
        - 确保课程代码不为空
        - 确保课程代码的唯一性
        """
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
        """
        验证学分字段的有效性
        - 确保学分为正数
        """
        if value <= 0:
            raise serializers.ValidationError('学分必须为正数')
        return value
    
    def validate_total_hours(self, value):
        """
        验证总课时字段的有效性
        - 确保总课时为正数
        """
        if value <= 0:
            raise serializers.ValidationError('总课时必须为正数')
        return value
    
    def get_teachers(self, obj):
        """\获取教授该课程的教师信息"""
        teachers = [ta.teacher for ta in obj.teaching_assignments.all()]
        return [{'id': teacher.id, 'name': teacher.name, 'title': teacher.title} for teacher in teachers]
    
    def get_student_count(self, obj):
        """\获取选修该课程的学生数量"""
        return obj.enrollments.count()

class EnrollmentSerializer(serializers.ModelSerializer):
    """
    学生选课序列化器，用于选课数据的序列化和反序列化
    """
    # 添加学生和课程的详细信息，方便前端显示
    student_name = serializers.ReadOnlyField(source='student.name')
    student_id = serializers.ReadOnlyField(source='student.student_id')
    course_name = serializers.ReadOnlyField(source='course.name')
    course_code = serializers.ReadOnlyField(source='course.code')
    
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'student_name', 'student_id', 'course_name', 'course_code', 
                  'enroll_date', 'score']
        read_only_fields = ['id', 'enroll_date']
    
    def validate_score(self, value):
        """
        验证成绩字段的有效性
        - 确保成绩在0-100之间
        """
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError('成绩必须在0-100之间')
        return value
    
    def validate(self, data):
        """
        验证学生是否已经选过该课程
        """
        student = data.get('student')
        course = data.get('course')
        
        # 检查学生是否已经选过该课程
        qs = Enrollment.objects.filter(student=student, course=course)
        if self.instance:
            qs = qs.exclude(id=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('该学生已经选过此课程')
        
        return data

class TeachingAssignmentSerializer(serializers.ModelSerializer):
    """
    教师授课序列化器，用于授课数据的序列化和反序列化
    """
    # 添加教师和课程的详细信息，方便前端显示
    teacher_name = serializers.ReadOnlyField(source='teacher.name')
    course_name = serializers.ReadOnlyField(source='course.name')
    course_code = serializers.ReadOnlyField(source='course.code')
    
    class Meta:
        model = TeachingAssignment
        fields = ['id', 'teacher', 'course', 'teacher_name', 'course_name', 'course_code', 
                  'assign_date', 'teaching_hours']
        read_only_fields = ['id', 'assign_date']
    
    def validate_teaching_hours(self, value):
        """
        验证授课课时字段的有效性
        - 确保授课课时为正数
        """
        if value <= 0:
            raise serializers.ValidationError('授课课时必须为正数')
        return value
    
    def validate(self, data):
        """
        验证教师是否已经被分配到该课程
        """
        teacher = data.get('teacher')
        course = data.get('course')
        
        # 检查教师是否已经被分配到该课程
        qs = TeachingAssignment.objects.filter(teacher=teacher, course=course)
        if self.instance:
            qs = qs.exclude(id=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('该教师已经被分配到这门课程')
        
        return data

class CourseWithDetailsSerializer(CourseSerializer):
    """\扩展的课程序列化器，包含更多详细信息"""
    # 包含选课和授课的详细信息
    enrollments = EnrollmentSerializer(many=True, read_only=True)
    teaching_assignments = TeachingAssignmentSerializer(many=True, read_only=True)
    
    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['enrollments', 'teaching_assignments']


class ClassroomSerializer(serializers.ModelSerializer):
    """
    教室序列化器，用于教室数据的序列化和反序列化
    """
    class Meta:
        model = Classroom
        fields = ['id', 'name', 'location', 'capacity', 'equipment']
        read_only_fields = ['id']
    
    def validate_capacity(self, value):
        """
        验证教室容量的有效性
        - 确保容量为正数
        """
        if value <= 0:
            raise serializers.ValidationError('教室容量必须为正数')
        return value


class ScheduleSerializer(serializers.ModelSerializer):
    """
    排课序列化器，用于排课数据的序列化和反序列化
    """
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
        """
        验证星期几的有效性
        - 确保星期几在1-7之间
        """
        if value < 1 or value > 7:
            raise serializers.ValidationError('星期几必须在1-7之间')
        return value
    
    def validate_start_section(self, value):
        """
        验证开始节次的有效性
        - 确保开始节次为正数
        """
        if value <= 0:
            raise serializers.ValidationError('开始节次必须为正数')
        return value
    
    def validate_end_section(self, value):
        """
        验证结束节次的有效性
        - 确保结束节次为正数
        """
        if value <= 0:
            raise serializers.ValidationError('结束节次必须为正数')
        return value
    
    def validate(self, data):
        """
        验证开始节次和结束节次的关系，以及排课冲突
        """
        # 验证开始节次小于结束节次
        if data.get('start_section') and data.get('end_section'):
            if data['start_section'] >= data['end_section']:
                raise serializers.ValidationError('开始节次必须小于结束节次')
        
        # 验证排课冲突（这里可以根据需要添加更复杂的冲突检测逻辑）
        # 注意：更复杂的冲突检测应该在视图层实现
        
        return data