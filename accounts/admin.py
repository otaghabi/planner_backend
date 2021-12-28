from django.contrib import admin
from django.contrib.admin import ModelAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(ModelAdmin):
    # TODO complete user admin manager
    pass
