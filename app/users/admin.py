from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserProfileAdmin(UserAdmin):

    list_display = (
        'email', 'first_name', 'last_name',
        'is_staff', 'is_superuser', 'is_active',
        'created',
    )
    list_filter = (
        'is_staff', 'is_superuser', 'is_active',
        'created', 'modified',
    )
    fieldsets = (
        (None, {
            'fields': ('email', 'password', 'uuid', 'token')
        }),
        ('Personal Data', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_superuser', 'is_staff', 'is_active')
        }),
        ('Timestamp', {
            'fields': ('created', 'modified')
        }),
    )
    search_fields = (
        'pk', 'email', 'first_name', 'last_name',
    )
    ordering = ('-created',)
    readonly_fields = ('uuid', 'token', 'is_superuser', 'is_staff',
                       'is_active', 'created', 'modified')
    date_hierarchy = 'created'