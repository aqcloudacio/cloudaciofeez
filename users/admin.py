# Register your models here.
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import AFSL
User = get_user_model()


class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {
            'fields':
                ('email', 'password')
                }),
        ('Personal info', {
            'fields':
                ('first_name', 'last_name')
            }),
        ('AFSL Details', {
            'fields':
                ('AFSL', 'active_rp', 'AFSL_approved', 'linked_ARN')
            }),
        ('Practice Details', {
            'fields':
                ('practices', 'admin_practices', 'pending_practices')
            }),
        ('Permissions', {
            'fields':
                ('is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions')
            }),
        ('Important dates', {
            'fields':
                ('last_login', 'date_joined')
            }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(User, UserAdmin)
admin.site.register(AFSL)
