# 课程管理模块模型扩展设计方案

## 一、现有模型结构概述

当前课程模块包含以下核心模型：
1. **Course** - 课程基本信息
2. **Enrollment** - 学生选课记录
3. **TeachingAssignment** - 教师授课记录

## 二、模型扩展设计方案

### 1. Course模型扩展

```python
class Course(models.Model):
    # 原有字段保留
    name = models.CharField(max_length=200, verbose_name='课程名称')
    code = models.CharField(max_length=50, unique=True, verbose_name='课程代码')
    credits = models.FloatField(verbose_name='学分')
    description = models.TextField(blank=True, null=True, verbose_name='课程描述')
    total_hours = models.IntegerField(verbose_name='总课时')
    semester = models.CharField(max_length=50, verbose_name='开设学期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 新增字段
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
    max_students = models.IntegerField(
        default=100,
        verbose_name='最大选课人数'
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程管理'
```

### 2. 新增Classroom模型

```python
class Classroom(models.Model):