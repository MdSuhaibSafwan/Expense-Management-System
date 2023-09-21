from django.shortcuts import redirect
from .models import Expense
from .forms import ExpenseAdminReportForm
from django.contrib import messages


def create_xl_report_for_expense(request):
    form = ExpenseAdminReportForm(data=request.POST)
    if not form.is_valid():
        print(form.errors)
        messages.error(request, message="Provide date")
    
    return redirect("/admin/expense/expense/", )


