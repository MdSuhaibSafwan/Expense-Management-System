from django.contrib import admin
from .models import AccountType, Account
from lib.admin import BaseAdmin


class AccountAdmin(BaseAdmin):
	pass


class AccountTypeAdmin(BaseAdmin):
	pass


admin.site.register(Account, AccountAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
