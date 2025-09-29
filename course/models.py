from django.db import models

"""
课程应用的数据模型定义
包含课程、学生选课、教师授课等核心实体
"""
from django.db import models
from django.db.models import Count

class Course(models.Model):
    """课程模型类，定义课程实体的数据结构
    根据课程表修复方案文档实现
    """
    # 课程信息字段定义
    name = models.CharField(max_length=200, verbose_name='课程名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='课程代码')
    
    # 课程类型 - 枚举类型
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
    
    # 授课方式 - 枚举类型
    TEACHING_METHOD_CHOICES = (
        ('online', '线上'),
        ('offline', '线下'),
    )
    teaching_method = models.CharField(
        max_length=10,
        choices=TEACHING_METHOD_CHOICES,
        default='offline',
        verbose_name='授课方式'
    )
    
    # 其他必填字段
    credits = models.FloatField(verbose_name='学分')
    total_hours = models.IntegerField(verbose_name='总课时')
    
    # 教室关联 - 仅限线下课程使用
    classroom = models.ForeignKey(
        'Classroom',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='上课教室'
    )
    
    # 人数限制字段
    max_students = models.IntegerField(
        default=50,
        verbose_name='总人数上限'
    )
    
    # 扩展字段
    semester = models.CharField(max_length=50, verbose_name='开设学期')
    description = models.TextField(blank=True, null=True, verbose_name='课程描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    @property
    def current_students(self):
        """获取当前已选择该课程的学生数"""
        return self.enrollments.count()

    def __str__(self):
        """返回课程的字符串表示形式"""
        return self.name
    
    def save(self, *args, **kwargs):
        """重写save方法，自动处理线上课程的容量设置和教室关联"""
        if self.teaching_method == 'online':
            # 线上课程固定容量为1000，清空教室关联
            self.max_students = 1000
            self.classroom = None
        elif self.teaching_method == 'offline' and self.classroom:
            # 线下课程取教室容量
            self.max_students = self.classroom.capacity
        
        super().save(*args, **kwargs)
    
    class Meta:
        """模型的元数据配置"""
        verbose_name = '课程'
        verbose_name_plural = '课程管理'

class Classroom(models.Model):
    """教室模型，定义教室实体的数据结构
    根据课程表修复方案文档实现
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='教室编号/名称')
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

class TeachingAssignment(models.Model):
    """教师授课模型，实现教师与课程的多对多关联
    根据课程表修复方案文档实现
    """
    teacher = models.ForeignKey(
        'teacher.Teacher', 
        on_delete=models.CASCADE, 
        related_name='teaching_assignments', 
        verbose_name='教师'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='teaching_assignments', 
        verbose_name='课程'
    )
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

class Enrollment(models.Model):
    """学生选课模型，实现学生与课程之间的关联关系
    根据课程表修复方案文档实现选课逻辑
    """
    student = models.ForeignKey(
        'student.Student', 
        on_delete=models.CASCADE, 
        related_name='enrollments', 
        verbose_name='学生'
    )
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='enrollments', 
        verbose_name='课程'
    )
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

class Schedule(models.Model):
    """排课模型，定义课程表实体的数据结构
    用于详细排课信息管理
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
