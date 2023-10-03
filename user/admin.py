from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

admin.site.unregister(Group)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ['email', 'username', 'is_author', 'is_checker', 'is_maker', 'is_active', 
                    'is_staff', 'is_superuser']
    list_filter = ['is_superuser', 'is_staff', 'is_active']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', )}),
        ('Permissions', {'fields': ('is_superuser', 'is_active', 'is_staff'),}),
        ('Expense Permissions', {'fields': ('is_author', 'is_checker', 'is_maker')}),
        # ('Groups', {'fields': ('groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
