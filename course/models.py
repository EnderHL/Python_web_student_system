from django.db import models

"""
课程应用的数据模型定义
包含课程、学生选课、教师授课等核心实体
"""
from django.db import models

class Course(models.Model):
    """课程模型类，定义课程实体的数据结构
    
    字段说明：
    - name: 课程名称，最大长度200字符
    - code: 课程代码，唯一标识，最大长度50字符
    - credits: 学分，浮点数类型
    - description: 课程描述，文本类型
    - total_hours: 总课时
    - semester: 开设学期，最大长度50字符
    - created_at: 创建时间，自动设置
    - updated_at: 更新时间，自动更新
    - course_type: 课程类型，必修课或选修课
    - max_students: 最大选课人数限制
    """
    name = models.CharField(max_length=200, verbose_name='课程名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='课程代码')
    credits = models.FloatField(verbose_name='学分')
    description = models.TextField(blank=True, null=True, verbose_name='课程描述')
    total_hours = models.IntegerField(verbose_name='总课时')
    semester = models.CharField(max_length=50, verbose_name='开设学期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 新增字段：课程类型
    COURSE_TYPE_CHOICES = (
        ('required', '必修课'),
        ('elective', '选修课'),
    )
    course_type = models.CharField(
        max_length=10,
        choices=COURSE_TYPE_CHOICES,
        default='required',
        verbose_name='课程类型'
    )
    # 新增字段：最大选课人数
    max_students = models.IntegerField(
        default=100,
        verbose_name='最大选课人数'
    )

    def __str__(self):
        """返回课程的字符串表示形式，使用课程名称"""
        return self.name
    
    class Meta:
        """模型的元数据配置"""
        verbose_name = '课程'
        verbose_name_plural = '课程管理'

class Enrollment(models.Model):
    """学生选课模型，定义学生与课程之间的多对多关联关系
    
    字段说明：
    - student: 关联的学生，使用ForeignKey
    - course: 关联的课程，使用ForeignKey
    - enroll_date: 选课日期，自动设置
    - score: 成绩，浮点数类型，可为空
    """
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE, related_name='enrollments', verbose_name='学生')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name='课程')
    enroll_date = models.DateTimeField(auto_now_add=True, verbose_name='选课日期')
    score = models.FloatField(blank=True, null=True, verbose_name='成绩')
    
    class Meta:
        """模型的元数据配置，确保一名学生对同一门课程只能有一条记录"""
        verbose_name = '选课记录'
        verbose_name_plural = '选课管理'
        unique_together = ('student', 'course')
    
    def __str__(self):
        """返回选课记录的字符串表示形式"""
        return f'{self.student.name} - {self.course.name}'

class TeachingAssignment(models.Model):
    """教师授课模型，定义教师与课程之间的多对多关联关系
    
    字段说明：
    - teacher: 关联的教师，使用ForeignKey
    - course: 关联的课程，使用ForeignKey
    - assign_date: 授课分配日期，自动设置
    - teaching_hours: 授课课时
    """
    teacher = models.ForeignKey('teacher.Teacher', on_delete=models.CASCADE, related_name='teaching_assignments', verbose_name='教师')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='teaching_assignments', verbose_name='课程')
    assign_date = models.DateTimeField(auto_now_add=True, verbose_name='分配日期')
    teaching_hours = models.IntegerField(verbose_name='授课课时')
    
    class Meta:
        """模型的元数据配置，确保一名教师对同一门课程只能有一条记录"""
        verbose_name = '授课记录'
        verbose_name_plural = '授课管理'
        unique_together = ('teacher', 'course')
    
    def __str__(self):
        """返回授课记录的字符串表示形式"""
        return f'{self.teacher.name} - {self.course.name}'


class Classroom(models.Model):
    """教室模型，定义教室实体的数据结构
    
    字段说明：
    - name: 教室名称
    - location: 教室位置
    - capacity: 教室容量
    - equipment: 教室设备描述
    """
    name = models.CharField(max_length=100, verbose_name='教室名称')
    location = models.CharField(max_length=200, verbose_name='教室位置')
    capacity = models.IntegerField(verbose_name='教室容量')
    equipment = models.TextField(blank=True, null=True, verbose_name='教室设备')
    
    def __str__(self):
        """返回教室的字符串表示形式"""
        return self.name
    
    class Meta:
        """模型的元数据配置"""
        verbose_name = '教室'
        verbose_name_plural = '教室管理'


class Schedule(models.Model):
    """排课模型，定义课程表实体的数据结构
    
    字段说明：
    - course: 关联的课程
    - classroom: 关联的教室
    - teaching_assignment: 关联的授课记录
    - day_of_week: 星期几上课
    - start_section: 开始节次
    - end_section: 结束节次
    - week_pattern: 上课周模式（单周、双周、每周）
    """
    WEEK_PATTERN_CHOICES = (
        ('all', '每周'),
        ('odd', '单周'),
        ('even', '双周'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules', verbose_name='课程')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='schedules', verbose_name='教室')
    teaching_assignment = models.ForeignKey(TeachingAssignment, on_delete=models.CASCADE, related_name='schedules', verbose_name='授课记录')
    day_of_week = models.IntegerField(verbose_name='星期几')  # 1-7表示周一到周日
    start_section = models.IntegerField(verbose_name='开始节次')
    end_section = models.IntegerField(verbose_name='结束节次')
    week_pattern = models.CharField(
        max_length=10,
        choices=WEEK_PATTERN_CHOICES,
        default='all',
        verbose_name='上课周模式'
    )
    
    def __str__(self):
        """返回排课记录的字符串表示形式"""
        return f'{self.course.name} - {self.classroom.name} - 星期{self.day_of_week}'
    
    class Meta:
        """模型的元数据配置，确保排课冲突检查"""
        verbose_name = '排课记录'
        verbose_name_plural = '排课管理'
        unique_together = (
            ('classroom', 'day_of_week', 'start_section', 'week_pattern'),  # 防止教室排课冲突
            ('teaching_assignment', 'day_of_week', 'start_section', 'week_pattern'),  # 防止教师排课冲突
        )
