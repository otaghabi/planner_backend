from django.contrib import admin

from accounts.models import User, Student, Advisor


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # TODO complete user admin manager
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    pass
