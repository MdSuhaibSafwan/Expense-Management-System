from .models import Expense
from django.db.models import Q

def get_expense_from_dates(date1, date2):
    qs = Expense.objects.filter(Q(date_created__gte=date1) & Q(date_created__lte=date2))
    return qs
