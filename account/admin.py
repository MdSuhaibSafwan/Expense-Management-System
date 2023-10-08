from django.contrib import admin
from .models import AccountType, Account, FundTransfer, FundApproveResponse, FundCheckResponse
from lib.admin import BaseAdmin


class FundTransferAdmin(BaseAdmin):
	pass


class AccountAdmin(BaseAdmin):
	list_display = ["account_no", "routing_no", "account_type", "date_created"]


class AccountTypeAdmin(BaseAdmin):
	pass


class FundApproveResponseAdmin(BaseAdmin):
	pass


class FundCheckResponseAdmin(BaseAdmin):
	pass



admin.site.register(Account, AccountAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(FundApproveResponse, FundApproveResponseAdmin)
admin.site.register(FundCheckResponse, FundCheckResponseAdmin)
admin.site.register(FundTransfer, FundTransferAdmin)
