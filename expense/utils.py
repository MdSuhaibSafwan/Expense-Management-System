from .models import Expense
from django.db.models import Q
from openpyxl import Workbook

def get_expense_from_dates(date1, date2):
    qs = Expense.objects.filter(Q(date_created__gte=date1) & Q(date_created__lte=date2))
    return qs


def generate_excel_file_based_on_qs(queryset, response):
    wb = Workbook()
    ws = wb.active
    ws.title = "Expenses"
    headers = ["Date", "Title", "Category Name", "Pending", "Completed", "status"]
    ws.append(headers)
    
    for expense in queryset:
        status = "not completed not approved"
        lst = ["null", "null", status]
        if expense.is_completed:
            status = "Completed"
            lst = ["null", expense.cost, status]

        elif expense.is_approved:
            status = "Approved"
            lst = [expense.cost, "null", status]

        final_list = [str(expense.date_created.date()), expense.title, expense.category.name, ]
        final_list.extend(lst)
        ws.append(final_list)

    
    wb.save(response)    
    return wb, response
