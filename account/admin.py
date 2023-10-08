from django.contrib import admin
from .models import AccountType, Account
from lib.admin import BaseAdmin


class AccountAdmin(BaseAdmin):
	list_display = ["account_no", "routing_no", "account_type", "date_created"]


class AccountTypeAdmin(BaseAdmin):
	pass


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
