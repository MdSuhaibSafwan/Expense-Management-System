from django.contrib import admin
from django.contrib import messages
from .models import Expense, Category
from .forms import ExpenseAdminForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.http import HttpResponse
from .utils import generate_excel_file_based_on_qs
from bank.models import BankCashout


class ExpenseAdmin(admin.ModelAdmin):
    change_list_template = "admin/expense/expense_list.html"
    list_display = ["category", "cost", "date_created"]
    form = ExpenseAdminForm
    model = Expense
    search_fields = ["category__name"]
    
    @admin.action(description='Generate Excel file')
    def generate_excel_file(self, request, queryset):
        return self._generate_excel_file(request, queryset)

    actions = [generate_excel_file, ]

    def get_form(self, request, obj=None, **kwargs):
                    
        return super().get_form(request, obj, **kwargs)
    
    def _generate_excel_file(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment;filename="report.xlsx"'
        wb, response = generate_excel_file_based_on_qs(queryset, response)
        # messages.success(request, "Excel file downloaded successfully")
        return response
    
    def add_view(self, request, form_url=None, extra_context=None):
        has_balance_obj = BankCashout.objects.has_latest_approved_object()
        if not has_balance_obj:
            messages.error(request, "Don't have enough balance")
            return redirect("/admin")
        return super().add_view(request, form_url, extra_context)
    
    def change_view(self, request, object_id, form_url=None, extra_context=None):
        has_balance_obj = BankCashout.objects.has_latest_approved_object()
        if not has_balance_obj:
            messages.error(request, "Don't have enough balance")
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
    
    def connect_to_bank(self):
        pass
    

admin.site.register(Category)
admin.site.register(Expense, ExpenseAdmin)
