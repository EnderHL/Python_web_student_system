"""
教师应用的数据模型定义
包含教师、角色、教师-角色关联、教师-课程关联等核心实体
"""
from django.db import models
from django.contrib.auth.models import Permission

class Teacher(models.Model):
    """教师模型类，定义教师实体的数据结构
    
    字段说明：
    - name: 教师姓名，最大长度100字符
    - age: 教师年龄
    - gender: 教师性别，最大长度10字符
    - title: 教师职称，最大长度100字符
    - department: 所属部门，最大长度100字符
    - email: 邮箱地址，唯一标识，最大长度100字符
    - phone: 联系电话，最大长度20字符
    - avatar: 头像图片，存储在teacher_avatars目录下
    - hire_date: 入职日期
    - created_at: 创建时间，自动设置
    - updated_at: 更新时间，自动更新
    """
    # 与用户认证系统集成，建立一对一关联
    user = models.OneToOneField('user_auth.CustomUser', on_delete=models.CASCADE, related_name='teacher_info', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')
    gender = models.CharField(max_length=10, verbose_name='性别')
    title = models.CharField(max_length=100, verbose_name='职称')
    department = models.CharField(max_length=100, verbose_name='所属部门')
    email = models.EmailField(max_length=100, unique=True, verbose_name='邮箱')
    phone = models.CharField(max_length=20, verbose_name='联系电话')
    # 暂时使用CharField代替ImageField，避免依赖Pillow库
    avatar = models.CharField(max_length=255, null=True, blank=True, verbose_name='头像URL')
    hire_date = models.DateField(verbose_name='入职日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        """返回教师的字符串表示形式，使用教师姓名"""
        return self.name

class Role(models.Model):
    """角色模型类，定义教师角色实体的数据结构

    字段说明：
    - name: 角色名称，唯一标识，最大长度100字符
    - description: 角色描述，可为空
    - permissions: 与权限模型的多对多关联
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='角色描述')
    permissions = models.ManyToManyField('auth.Permission', blank=True, verbose_name='权限列表')

    def __str__(self):
        """返回角色的字符串表示形式，使用角色名称"""
        return self.name

class TeacherRole(models.Model):
    """教师角色关联模型类，定义教师与角色的多对多关联关系
    
    字段说明：
    - teacher: 与教师模型的外键关联
    - role: 与角色模型的外键关联
    - assigned_at: 角色分配时间，自动设置
    
    约束：
    - 教师与角色的组合必须唯一
    """
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='教师')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='角色')
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='分配时间')

    class Meta:
        unique_together = ('teacher', 'role')
        verbose_name = '教师角色关联'
        verbose_name_plural = '教师角色关联'

    def __str__(self):
        """返回教师角色关联的字符串表示形式"""
        return f'{self.teacher.name} - {self.role.name}'

# 保留此模型的注释代码，当前因课程应用尚未开发或未集成而暂时注释
# 当课程应用可用时，需要取消注释并修改为实际的课程外键关联
# class TeacherCourse(models.Model):
#     """教师课程关联模型类，定义教师与课程的多对多关联关系
#     
#     字段说明：
#     - teacher: 与教师模型的外键关联
#     - course: 与课程模型的外键关联
#     - start_date: 课程开始日期
#     - end_date: 课程结束日期
#     - created_at: 创建时间，自动设置
#     
#     约束：
#     - 教师、课程与开始日期的组合必须唯一
#     """
#     teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='教师')
#     # course = models.ForeignKey('course.Course', on_delete=models.CASCADE, verbose_name='课程')
#     course_name = models.CharField(max_length=100, verbose_name='课程名称')
#     start_date = models.DateField(verbose_name='开始日期')
#     end_date = models.DateField(verbose_name='结束日期')
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
# 
#     class Meta:
#         unique_together = ('teacher', 'course_name', 'start_date')
#         verbose_name = '教师课程关联'
#         verbose_name_plural = '教师课程关联'
# 
#     def __str__(self):
#         """返回教师课程关联的字符串表示形式"""
#         return f'{self.teacher.name} - {self.course_name}'
