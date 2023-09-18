from django.contrib import admin
from django.contrib import messages
from .models import Expense, Category
from .forms import ExpenseAdminForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["category", "cost", "quantity", "is_approved", "is_completed"]
    form = ExpenseAdminForm

    def get_form(self, request, obj=None, **kwargs):
        user = request.user
        if not self.check_is_user_valid(user):
            raise PermissionDenied("User do not have any permission")
        if user.is_author:
            self.readonly_fields = ["is_approved", "is_completed"]
        if user.is_checker:
            self.readonly_fields = ["category", "quantity",  "cost", "is_completed"]
        if user.is_maker:
            self.readonly_fields = ["category", "cost", "quantity", "is_approved",]
        
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        return form
    
    def add_view(self, request, form_url=None, extra_context=None):
        if not self.check_is_user_valid(request.user):
            messages.error(request, "User not permitted to manage expenses")
            return redirect("/admin")
        return super().add_view(request, form_url, extra_context)
    
    def change_view(self, request, object_id, form_url=None, extra_context=None):
        if not self.check_is_user_valid(request.user):
            messages.error(request, "User not permitted to manage expenses")
            return redirect("/admin")

        return super().change_view(request, object_id, form_url, extra_context)
    
    def check_is_user_valid(self, user):
        return getattr(user, "is_author", getattr(user, "is_checker", getattr(user, "is_maker", None)))
        

admin.site.register(Category)
admin.site.register(Expense, ExpenseAdmin)
