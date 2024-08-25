from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, School

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('display_name', 'school')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'display_name', 'school'),
        }),
    )
    list_display = ('username', 'email', 'display_name', 'school', 'is_staff')
    search_fields = ('username', 'email', 'display_name', 'school__name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(School)