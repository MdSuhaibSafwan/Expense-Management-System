import custom_admin as admin
from django.urls import path, include

urlpatterns = [
    path("", include("expense.urls")),
    path("", admin.site.urls),
]
