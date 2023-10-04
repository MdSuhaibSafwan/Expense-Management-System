from django.contrib import admin
from .models import BankAccount, BankCashout
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import BankCashoutForm


class BankAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "open_balance"]


class BankCashoutAdmin(admin.ModelAdmin):
    list_display = ["id", "bank", "cash", "is_approved", "is_completed"]
    form = BankCashoutForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        user = request.user
        self.request = request
        self.object = obj
        if not self.check_is_user_valid(user):
            raise PermissionDenied("User not permitted to do so")

        if self.action_view == "change_view":
            form.change_view = self.action_view
            form.cashout_obj = obj
        
        self.make_readonly_field_according_to_user(user)
        return form
    
    def make_readonly_field_according_to_user(self, user):
        if user.is_author:
            self.readonly_fields = ["is_approved", "is_completed"]

        if user.is_checker:
            self.readonly_fields = ["title", "bank", "cash", "is_completed"]
            
        if user.is_maker:
            self.readonly_fields = ["title", "bank", "cash", "is_approved"]

        if self.object is None:
            if not self.request.user.is_author:
                raise PermissionDenied("Not Applicabe to add expenses")

    def add_view(self, request, form_url=None, extra_context=None):
        self.action_view = "add_view"
        if not self.check_is_user_valid(request.user):
            messages.error(request, "User not permitted to manage expenses")
            return redirect("/admin")

        return super().add_view(request, form_url, extra_context)
    
    def change_view(self, request, object_id, form_url=None, extra_context=None):
        self.action_view = "change_view"
        if not self.check_is_user_valid(request.user):
            messages.error(request, "User not permitted to manage expenses")
            return redirect("/admin")

        return super().change_view(request, object_id, form_url, extra_context)
    
    def check_is_user_valid(self, user):
        return (user.is_author) or (user.is_checker) or (user.is_maker)

    def has_any_active_checkout(self):
        msg = ""
        return False, msg

    def is_expense_approved(self):
        msg = ""
        return False, msg


admin.site.register(BankAccount, BankAdmin)
admin.site.register(BankCashout, BankCashoutAdmin)
