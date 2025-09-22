from django.contrib import admin

"""
课程应用的管理界面配置
"""
from django.contrib import admin
from .models import Course, Enrollment, TeachingAssignment, Classroom, Schedule


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """课程模型的管理界面配置"""
    list_display = ('name', 'code', 'course_type', 'credits', 'total_hours', 'semester', 'max_students')
    search_fields = ('name', 'code')
    list_filter = ('course_type', 'semester')
    ordering = ('code',)
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'code', 'course_type', 'credits', 'total_hours', 'semester')
        }),
        ('其他信息', {
            'fields': ('description', 'max_students')
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """选课记录模型的管理界面配置"""
    list_display = ('student', 'course', 'enroll_date', 'score')
    search_fields = ('student__name', 'course__name')
    list_filter = ('course', 'enroll_date')
    ordering = ('-enroll_date',)


@admin.register(TeachingAssignment)
class TeachingAssignmentAdmin(admin.ModelAdmin):
    """授课记录模型的管理界面配置"""
    list_display = ('teacher', 'course', 'assign_date', 'teaching_hours')
    search_fields = ('teacher__name', 'course__name')
    list_filter = ('course', 'assign_date')
    ordering = ('-assign_date',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    """教室模型的管理界面配置"""
    list_display = ('name', 'location', 'capacity')
    search_fields = ('name', 'location')
    list_filter = ('capacity',)
    ordering = ('name',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    """排课记录模型的管理界面配置"""
    list_display = (
        'course', 'teacher', 'classroom', 
        'get_day_of_week', 'start_section', 'end_section', 'week_pattern'
    )
    search_fields = ('course__name', 'teacher__name', 'classroom__name')
    list_filter = ('week_pattern', 'day_of_week')
    ordering = ('day_of_week', 'start_section')
    
    def get_day_of_week(self, obj):
        """将数字星期转换为中文星期"""
        weekdays = {1: '周一', 2: '周二', 3: '周三', 4: '周四', 5: '周五', 6: '周六', 7: '周日'}
        return weekdays.get(obj.day_of_week, f'星期{obj.day_of_week}')
    
    get_day_of_week.short_description = '星期几'
    
    def teacher(self, obj):
        """显示授课教师"""
        return obj.teaching_assignment.teacher
    
    teacher.short_description = '教师'
