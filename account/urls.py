from django.urls import path
from .views import (
	fund_transfer_check_admin_view, fund_transfer_approve_admin_view, verify_otp_for_fund_check,
	verify_otp_for_fund_approve
)

urlpatterns = [
	path("check/", fund_transfer_check_admin_view, ),
	path("check/verify-otp/", verify_otp_for_fund_check, name="verify-check-otp"),
	path("approve/", fund_transfer_approve_admin_view, ),
	path("approve/verify-otp/", verify_otp_for_fund_approve, name="verify-approve-otp"),
]

