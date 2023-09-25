from django.shortcuts import redirect
from .models import Expense
from .forms import ExpenseAdminReportForm
from django.contrib import messages
from .utils import get_expense_from_dates, generate_excel_file_based_on_qs
from django.http import HttpResponse


def create_xl_report_for_expense(request):
    form = ExpenseAdminReportForm(data=request.POST)
    if not form.is_valid():
        messages.error(request, message=form.error_text)
        return redirect("/admin/expense/expense/", )
    
    date1 = form.cleaned_data.get("date1")
    date2 = form.cleaned_data.get("date2")
    qs = get_expense_from_dates(date1, date2)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename="report.xlsx"'
    wb, response = generate_excel_file_based_on_qs(qs, response)
    return response
