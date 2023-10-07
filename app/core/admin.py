"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import User, Message


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    list_filter = ['is_staff', 'is_active']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'), {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = [
        'email',
        'title',
    ]
    readonly_fields = ['created_at']
    list_filter = ['is_recent', 'is_read', 'is_answered']
    list_per_page = 20
