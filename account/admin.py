from django.contrib import admin
from .models import AccountType, Account, FundTransfer, FundApproveResponse, FundCheckResponse
from lib.admin import BaseAdmin


class FundTransferAdmin(BaseAdmin):
	list_display = ["from_account", "to_account", "amount", "is_approved", "is_checked"]


class AccountAdmin(BaseAdmin):
	list_display = ["account_no", "routing_no", "account_type", "opening_balance", "date_created"]


class AccountTypeAdmin(BaseAdmin):
	list_display = ["id", "name"]


class FundApproveResponseAdmin(BaseAdmin):
	pass


class FundCheckResponseAdmin(BaseAdmin):
	pass


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(FundApproveResponse, FundApproveResponseAdmin)
admin.site.register(FundCheckResponse, FundCheckResponseAdmin)
admin.site.register(FundTransfer, FundTransferAdmin)
