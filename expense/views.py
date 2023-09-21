from django.shortcuts import redirect
from .models import Expense
from .forms import ExpenseAdminReportForm
from django.contrib import messages
from .utils import get_expense_from_dates
from django.http import HttpResponse
from openpyxl import Workbook


def create_xl_report_for_expense(request):
    form = ExpenseAdminReportForm(data=request.POST)
    if not form.is_valid():
        messages.error(request, message="Please provide date correctly")
        return redirect("/admin/expense/expense/", )
    
    date1 = form.cleaned_data.get("date1")
    date2 = form.cleaned_data.get("date2")
    qs = get_expense_from_dates(date1, date2)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment;filename="report.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"

    # Add headers
    headers = ["Name", "Price", "Quantity", "Total Cost"]
    ws.append(headers)

    for expense in qs:
        ws.append([expense.category.name, expense.cost, expense.quantity, expense.total_cost(), ])

    wb.save(response)    
    return response


