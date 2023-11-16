from .models import Expense
from django.db.models import Q
from openpyxl import Workbook
from django.utils import timezone

def get_expense_from_dates(date1, date2):
    qs = Expense.objects.filter(Q(date_created__gte=date1) & Q(date_created__lte=date2))
    return qs


def generate_excel_file_based_on_qs(queryset, response):
    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"
    headers = ["Date", "User", "Title", "Category Name", "cost"]
    ws.append(headers)
    
    for expense in queryset:
        lst = [str(expense.date_created.date()), expense.user.email, expense.title, expense.category.name,
        str(expense.cost), ]
        ws.append(lst)

    
    wb.save(response)    
    return wb, response


def get_today_expense():
    now = timezone.now()
    return Expense.objects.filter(date_created=now)


def get_this_year_expense():
    now = timezone.now()
    return Expense.objects.filter(date_created__year=now.year)


def get_this_month_expense():
    now = timezone.now()
    return Expense.objects.filter(date_created__year=now.year, date_created__month=now.month)
