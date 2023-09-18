from django.contrib import admin
from .models import Expense, Category
from .forms import ExpenseAdminForm


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["category", "cost", "quantity", "is_approved", "is_completed"]
    form = ExpenseAdminForm

    def get_form(self, request, obj=None, **kwargs):
        user = request.user
        if user.is_author:
            self.readonly_fields = ["is_approved", "is_completed"]
        if user.is_checker:
            self.readonly_fields = ["category", "quantity",  "cost", "is_completed"]
        if user.is_maker:
            self.readonly_fields = ["category", "cost", "quantity", "is_approved",]
        
        form = super().get_form(request, obj, **kwargs)
        form.user = request.user
        return form


admin.site.register(Category)
admin.site.register(Expense, ExpenseAdmin)
