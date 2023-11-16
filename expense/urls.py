from django.urls import path
from .views import create_xl_report_for_expense

urlpatterns = [
    path("expense-report/", create_xl_report_for_expense, name="expense-report-xl"),
]
