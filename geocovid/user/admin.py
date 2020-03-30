from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserAdminCreationForm, UserAdminForm

from django.contrib.auth.models import Group, Permission


class UserAdmin(BaseUserAdmin):

    add_form = UserAdminCreationForm
    add_fieldsets = (
        (None, {
            'fields': ('name', 'email', 'password1', 'password2')
        }),
    )
    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('email',)
        }),
        ('Basic informations', {
            'fields': ('name', 'last_login')
        }),

        (
            'Permissions', {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser', 'groups',
                    'user_permissions'
                )
            }
        ),
    )
    list_display = ['name', 'email', 'is_active', 'is_staff', 'date_joined']


admin.site.register(User, UserAdmin)