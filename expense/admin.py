from django.contrib import admin
from django.contrib import messages
from .models import Expense, Category
from .forms import ExpenseAdminForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class ExpenseAdmin(admin.ModelAdmin):
    change_list_template = "admin/expense/expense_list.html"
    list_display = ["category", "cost", "quantity", "total_cost", "is_approved", "is_completed"]
    form = ExpenseAdminForm
    model = Expense
    search_fields = ["category__name"]
    list_filter = ["is_approved", "is_completed"]
    
    @admin.action(description='Generate Excel file')
    def generate_excel_file(self, request, queryset):
        return self._generate_excel_file(request, queryset)

    actions = [generate_excel_file, ]

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
        
        return super().get_form(request, obj, **kwargs)
    
    def _generate_excel_file(self, request, queryset):
        messages.success(request, "Excel file downloaded successfully")
        return redirect("/admin/expense/expense/")
    
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
        return (user.is_author) or (user.is_checker) or (user.is_maker)
    
    def get_total_expense(self):
        qs = self.model.objects.all()
        return self.sum_total_expense(qs)
    
    def get_approved_expense(self):
        qs = self.model.objects.filter(is_approved=True)
        return self.sum_total_expense(qs)
    
    def get_completed_expense(self):
        qs = self.model.objects.filter(is_completed=True)
        return self.sum_total_expense(qs)
    
    def sum_total_expense(self, qs):
        total = sum([i[0]*i[1] for i in list(qs.values_list("cost", "quantity"))])
        return total
    

admin.site.register(Category)
admin.site.register(Expense, ExpenseAdmin)
