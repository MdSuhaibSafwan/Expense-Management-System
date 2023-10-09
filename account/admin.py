from django.contrib import admin
from .models import AccountType, Account, FundTransfer, FundApprove, FundCheck
from lib.admin import BaseAdmin
from .forms import FundTransferForm


class FundApproveInline(admin.TabularInline):
	model = FundApprove
	fields = ["description", "is_approved"]


class FundCheckInline(admin.TabularInline):
	model = FundCheck
	fields = ["description", "is_checked"]


class FundTransferAdmin(BaseAdmin):
	form = FundTransferForm
	list_display = ["id", "from_account", "to_account", "amount", "is_approved", "is_checked"]
	fieldsets = (
		('Accounts', {'fields': ('from_account', 'to_account', )}),
		('Others', {'fields': ('amount', 'description')})
	)

	add_fieldsets = fieldsets

	def get_form(self, *args, **kwargs):
		form = super().get_form(*args, **kwargs)
		form.action_view = self.action_view
		return form

	def add_view(self, request, *args, **kwargs):
		self.action_view = "add_view"
		self.add_tabular_inline_according_to_user(request.user)
		self.add_readonly_fields_according_to_user(request.user)
		return super().add_view(request, *args, **kwargs)

	def change_view(self, request, *args, **kwargs):
		self.action_view = "change_view"
		self.add_readonly_fields_according_to_user(request.user)
		self.add_tabular_inline_according_to_user(request.user)
		return super().change_view(request, *args, **kwargs)

	def add_readonly_fields_according_to_user(self, user):
		if not user.is_author:
			self.readonly_fields = ["from_account", "to_account", "amount", "description"]

	def add_tabular_inline_according_to_user(self, user):
		if user.is_checker:
			self.inlines = [FundCheckInline, ]

		if user.is_approver:
			self.inlines = [FundApproveInline, ]


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
