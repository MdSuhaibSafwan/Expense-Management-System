from django.contrib import admin
from .models import AccountType, Account, FundTransfer, FundApprove, FundCheck
from lib.admin import BaseAdmin
from .forms import FundTransferForm


class FundTransferAdmin(BaseAdmin):
	form = FundTransferForm
	list_display = ["id", "from_account", "to_account", "amount", "is_approved", "is_checked"]
	fieldsets = (
		('Accounts', {'fields': ('from_account', 'to_account', )}),
		('Others', {'fields': ('amount', 'description')})
	)

	add_fieldsets = fieldsets


class AccountAdmin(BaseAdmin):
	list_display = ["account_no", "routing_no", "account_type", "opening_balance", "date_created"]


class AccountTypeAdmin(BaseAdmin):
	list_display = ["id", "name"]


class FundApproveAdmin(BaseAdmin):
	pass


class FundCheckAdmin(BaseAdmin):
	pass


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(FundApprove, FundApproveAdmin)
admin.site.register(FundCheck, FundCheckAdmin)
admin.site.register(FundTransfer, FundTransferAdmin)
