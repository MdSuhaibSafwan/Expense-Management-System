from django.contrib import admin
from .models import AccountType, Account, FundTransfer, FundApprove, FundCheck
from lib.admin import BaseAdmin
from .forms import FundTransferForm, FundApproveForm, FundCheckForm, FundCheckFormSet, FundApproveFormSet


class FundApproveInline(admin.TabularInline):
	model = FundApprove
	form = FundApproveForm
	formset = FundApproveFormSet
	fields = ["description", "is_approved"]

	def get_formset(self, request, obj=None, *args, **kwargs):
		formset = super().get_formset(request, *args, **kwargs)
		formset.request = request
		formset.fund_transfer_obj = obj
		return formset


class FundCheckInline(admin.TabularInline):
	model = FundCheck
	form = FundCheckForm
	formset = FundCheckFormSet
	fields = ["description", "is_checked"]

	def get_formset(self, request, obj=None, *args, **kwargs):
		formset = super().get_formset(request, *args, **kwargs)
		formset.request = request
		formset.fund_transfer_obj = obj
		return formset


class FundTransferAdmin(BaseAdmin):
	form = FundTransferForm
	list_display = ["id", "from_account", "to_account", "amount", "approved", "checked"]
	fieldsets = (
		('Accounts', {'fields': ('from_account', 'to_account', )}),
		('Others', {'fields': ('amount', 'description')})
	)

	add_fieldsets = fieldsets
	check_fund_transfer_validation = True

	def get_form(self, *args, **kwargs):
		form = super().get_form(*args, **kwargs)
		form.action_view = self.action_view
		form.check_validation = self.check_fund_transfer_validation
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
		if user.is_superuser:
			self.check_fund_transfer_validation = True
			return None

		if user.is_checker:
			self.check_fund_transfer_validation = False
			self.inlines = [FundCheckInline, ]

		if user.is_approver:
			self.check_fund_transfer_validation = False
			self.inlines = [FundApproveInline, ]

	# def save_formset(self, request, obj, formset, change):
	# 	instances = formset.save(commit=True)
	# 	print("Request ", request)
	# 	print("Obj ", obj)
	# 	print("Change ", change)
	# 	print("Instance ", instances)

	# def save_model(self, request, obj, form, change):
	# 	print("OBJ ", obj)

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
