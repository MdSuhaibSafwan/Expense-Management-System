from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path("admin/create-report/", create_xl_report_for_expense),
    path('admin/', admin.site.urls),
    # path("api/", include("expense.api.urls")),
]
