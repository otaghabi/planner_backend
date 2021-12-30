from django.contrib import admin

from planners.models import Course, Task


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
