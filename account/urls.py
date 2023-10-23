from django.urls import path
from .views import fund_transfer_check_admin_view, fund_transfer_approve_admin_view

urlpatterns = [
	path("check/", fund_transfer_check_admin_view, ),
	path("approve/", fund_transfer_approve_admin_view, )
]

