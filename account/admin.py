from admin_site import admin
from .models import AccountType, Account, FundTransfer, FundApprove, FundCheck
from lib.admin import BaseAdmin
from .forms import FundTransferForm, FundApproveForm, FundCheckForm, FundCheckFormSet, FundApproveFormSet, \
	AccountTypeForm, AccountForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


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
	fields = ["description", "is_checked", "approver_assignee"]

	def get_formset(self, request, obj=None, *args, **kwargs):
		formset = super().get_formset(request, *args, **kwargs)
		formset.request = request
		formset.fund_transfer_obj = obj
		return formset


class FundTransferAdmin(BaseAdmin):
	change_form_template = "admin/account/fund_transfer_change.html"
	form = FundTransferForm
	list_display = ["id", "from_account", "to_account", "amount", "approved", "checked", "is_approved", "is_checked"]
	fieldsets = (
		('Accounts', {'fields': ('from_account', 'to_account', )}),
		('Others', {'fields': ('amount', 'description')}),
		("Assigner", {'fields': ("checker_assignee", )})
	)

	add_fieldsets = fieldsets
	check_fund_transfer_validation = True

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj=None, **kwargs)
		self.obj = obj
		form.action_view = self.action_view
		form.check_validation = self.check_fund_transfer_validation
		return form

	def add_view(self, request, *args, **kwargs):
		self.action_view = "add_view"
		self.add_readonly_fields_according_to_user(request.user)
		return super().add_view(request, *args, **kwargs)

	def change_view(self, request, object_id, extra_content=None):
		self.action_view = "change_view"
		self.object_id = object_id
		self.request = request
		self.form_extras = {
			"extra_form": None
		}
		self.add_readonly_fields_according_to_user(request.user)
		self.add_tabular_inline_according_to_user(request.user)
		change_view =  super().change_view(request, object_id, extra_content)
		change_view.context_data.update({"form_extras": self.form_extras})
		context = change_view.context_data
		return change_view

	def get_object(self, request, object_id, from_field=None):
		try:
			obj = self.object
			return obj
		except Exception as e:
			pass

		try:
			obj = FundTransfer.objects.get(id=object_id)
		except ObjectDoesNotExist:
			return None

		return obj

	def add_readonly_fields_according_to_user(self, user):
		if not user.is_author:
			self.readonly_fields = ["from_account", "to_account", "amount", "description", "checker_assignee"]
			print("Made read only fields")

	def add_tabular_inline_according_to_user(self, user):
		obj = self.get_object(self.request, self.object_id)
		if user.is_superuser:
			self.check_fund_transfer_validation = True
			return None

		if user.is_checker:
			self.check_fund_transfer_validation = False
			if (obj.checker_assignee != user) and (obj.checker_assignee is not None):
				messages.error(self.request, "sorry you are not obliged to check this transfer")
				return None
			self.inlines = [FundCheckInline, ]
			try:
				form = FundCheckForm(instance=obj.checked_response)
			except ObjectDoesNotExist:
				form = FundCheckForm()

			self.form_extras.update({"extra_form": form, "form_name": "Checking Form", "form_action": "check"})

		if user.is_approver:
			fund_transfer_obj = self.get_object(self.request, self.object_id)
			if fund_transfer_obj is None:
				return None
			try:
				checked_obj = fund_transfer_obj.checked_response
			except ObjectDoesNotExist:
				messages.error(self.request, "Fund Transfer is not Checked")
				return None

			if not checked_obj.is_checked:
				messages.error(self.request, "Fund Transfer is not Checked")
			else:
				self.check_fund_transfer_validation = False
				if (checked_obj.approver_assignee != user) and (checked_obj.approver_assignee is not None):
					messages.error(self.request, "sorry you're not obliged to approve this transfer")
					return None
				self.inlines = [FundApproveInline, ]
				try:
					form = FundApproveForm(instance=obj.approval_response)
				except ObjectDoesNotExist:
					form = FundApproveForm()
				self.form_extras.update({"extra_form": form, "form_name": "Approval Form", "form_action": "approve"})
		# self.extra_content.update({"extra_form": self.inlines})


class AccountAdmin(BaseAdmin):
	list_display = ["account_no", "routing_no", "name", "account_type", "opening_balance", "date_created"]
	form = AccountForm


class AccountTypeAdmin(BaseAdmin):
	list_display = ["id", "name", ]
	form = AccountTypeForm


class FundApproveAdmin(BaseAdmin):
	list_display = ["id", "user", "fund_transfer", "is_approved", "is_2fa_verified", "is_completed"]



class FundCheckAdmin(BaseAdmin):
	list_display = ["id", "user", "fund_transfer", "is_checked", "is_2fa_verified", "is_completed"]



admin.site.register(Account, AccountAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(FundApprove, FundApproveAdmin)
admin.site.register(FundCheck, FundCheckAdmin)
admin.site.register(FundTransfer, FundTransferAdmin)
