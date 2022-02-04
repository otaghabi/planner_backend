from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User, Student, Advisor


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'avatar', 'first_name', 'last_name', 'gender', 'age', 'national_code'
        )}),
        ('Contact info', {'fields': (
            'phone_number',
        )}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_filter = ('gender', 'is_staff', 'is_superuser', 'is_active', 'groups')
    list_display = ('id', 'email', 'first_name', 'last_name', 'avatar', 'is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')
    list_editable = ('is_staff', 'is_active')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    pass
