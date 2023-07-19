from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    """
    User admin interface
    """
    pass

# Register the default User model with a custom ModelAdmin
admin.site.register(User, UserAdmin)
