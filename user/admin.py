from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User2FAAuth
from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ['email', 'is_author', 'is_checker', 'is_approver', 'is_active', 'is_staff', 'is_superuser']
    list_filter = ['is_superuser', 'is_staff', 'is_active']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', )}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_staff'),}),
        ('Groups', {'fields': ('groups', )})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']

class User2FAAuthAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "token"]


admin.site.register(User, UserAdmin)
admin.site.register(User2FAAuth, User2FAAuthAdmin)
