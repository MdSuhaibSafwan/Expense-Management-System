from django import forms
from .models import FundTransfer, FundApprove, FundCheck, AccountType, Account
from django.forms.models import BaseInlineFormSet 


class FundApproveForm(forms.ModelForm):
	is_changable = True

	class Meta:
		model = FundApprove
		exclude = ["fund_transfer", "user", "fund_check", "is_completed", "is_2fa_verified"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		instance = getattr(self, "instance", None)
		if instance:
			if (instance.is_2fa_verified) and (instance.is_completed):
				self.fields["description"].widget.attrs["disabled"] = "disabled"
				self.fields["is_approved"].widget.attrs["disabled"] = "disabled"
				setattr(self, "is_changable", False)


	def clean(self):
		data = super().clean()
		self.validate_fund_check()
		return data

	def validate_fund_check(self):
		if self.fc_obj.approver_assignee is None:
			return True

		return self.fc_obj.approver_assignee == self.user


class FundCheckForm(forms.ModelForm):
	is_changable = True
	
	class Meta:
		model = FundCheck
		# fields = "__all__"
		exclude = ["fund_transfer", "user", "is_completed", "is_2fa_verified"]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		instance = getattr(self, "instance", None)
		if instance:
			if (instance.is_2fa_verified) and (instance.is_completed):
				self.fields["description"].widget.attrs["disabled"] = "disabled"
				self.fields["is_checked"].widget.attrs["disabled"] = "disabled"
				self.fields["approver_assignee"].widget.attrs["disabled"] = "disabled"
				setattr(self, "is_changable", False)

	def clean(self):
		data = super().clean()
		approver_assignee = data.get("approver_assignee")
		if approver_assignee:
			if not approver_assignee.is_approver:
				self.add_error("approver_assignee", "User is cannot an approver")

		return data



class FundTransferForm(forms.ModelForm):

	class Meta:
		model = FundTransfer
		fields = "__all__"
		widgets = {
			'from_account': forms.Select(attrs={'class': 'form-control'}),
			'to_account': forms.Select(attrs={'class': 'form-control'}),
			'checker_assignee': forms.Select(attrs={'class': 'form-control'}),
			'amount': forms.NumberInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class': 'form-control'}),
		}

	def clean(self):
		data = super().clean()
		print("Val ", self.check_validation, )
		if not self.check_validation:
			return data
		from_account = data.get("from_account")
		to_account = data.get("to_account")
		if from_account == to_account:
			raise forms.ValidationError("Accounts Cannot transfer among themselves")

		amount = data.get("amount")
		if from_account is not None:
			if from_account.get_current_balance() < amount:
				raise forms.ValidationError("Insufficient Balance")
	
			self.validate_from_account(data)

		assigned_user = data.get("checker_assignee", None)

		if assigned_user is not None:
			self.validate_checker_assignee(assigned_user)

		return data

	def validate_from_account(self, data):
		from_account = data["from_account"]
		fund_transfer_obj = from_account.get_latest_outgoing_fund_transfer()
		if fund_transfer_obj is None:
			return from_account

		# if not ((fund_transfer_obj.is_approved()) and (fund_transfer_obj.is_checked())):
		# 	self.add_error("from_account", "Please Approve the previous Fund Transaction to apply again")

		self.validate_checking_response(fund_transfer_obj)
		self.validate_approval_response(fund_transfer_obj)
		return from_account

	def validate_checking_response(self, fund_transfer_obj):
		checker_resp_obj = fund_transfer_obj.get_checking_response()
		self.ft_checked_obj = checker_resp_obj
		if checker_resp_obj is None:
			self.add_error("from_account", "Please provide a check to fund transaction to apply again from this account")

		return True

	def validate_approval_response(self, fund_transfer_obj):
		approval_response_obj = fund_transfer_obj.get_approval_response()
		if approval_response_obj is None:
			checker_resp_obj = ft_checked_obj
			if checker_resp_obj.is_checked:
				self.add_error("from_account", "Please approve previous fund transaction to apply again from this account")

		return True

	def validate_checker_assignee(self, user):
		if not user.is_checker:
			self.add_error("checker_assignee", "User is not a Checker")

		return user


class FundCheckFormSet(BaseInlineFormSet):
	def save_new_objects(self, commit=True):
		saved_instances = super(FundCheckFormSet, self).save_new_objects(commit)
		if commit:
			pass
		return saved_instances

	def save_existing_objects(self, commit=True):
		saved_instances = super(FundCheckFormSet, self).save_existing_objects(commit)
		print("Saving existing object ", saved_instances)
		user = self.request.user
		fund_transfer_obj = self.fund_transfer_obj
		if not hasattr(fund_transfer_obj, "checked_response"):
			return saved_instances

		fund_check_obj = getattr(fund_transfer_obj, "checked_response")
		fund_check_obj.user = user
		fund_check_obj.save()
		return saved_instances

	def clean(self):
		super().clean()
		for form in self.forms:
			approver_assignee = form.cleaned_data.get("approver_assignee", None)
			if approver_assignee is not None:
				if not approver_assignee.is_approver:
					raise forms.ValidationError("User should be an Approver")




class FundApproveFormSet(BaseInlineFormSet):
	def save_new_objects(self, commit=True):
		saved_instances = super(FundApproveFormSet, self).save_new_objects(commit)
		if commit:
			pass
		return saved_instances

	def save_existing_objects(self, commit=True):
		saved_instances = super(FundApproveFormSet, self).save_existing_objects(commit)
		print("Saving existing object ", saved_instances)
		user = self.request.user
		fund_transfer_obj = self.fund_transfer_obj
		"""
			WORKS REMAINING HERE
		"""
		if not hasattr(fund_transfer_obj, "approval_response"):
			return saved_instances

		if not hasattr(fund_transfer_obj, "checked_response"):
			return saved_instances

		fund_check_obj = getattr(fund_transfer_obj, "checked_response")

		fund_approve_obj = getattr(fund_transfer_obj, "approval_response")
		fund_approve_obj.user = user
		fund_approve_obj.fund_check = fund_check_obj
		fund_approve_obj.save()

		if not hasattr(fund_transfer_obj, "approval_response"):
			return saved_instances

		print("Fund Approval Obj ", fund_approve_obj)

		return saved_instances


class AccountForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = "__all__"
		exclude = ["date_created"]
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'account_no': forms.TextInput(attrs={'class': 'form-control'}),
			'routing_no': forms.TextInput(attrs={'class': 'form-control'}),
			'opening_balance': forms.NumberInput(attrs={'class': 'form-control'}),
			'account_type': forms.Select(attrs={'class': 'form-control'}),
		}



class AccountTypeForm(forms.ModelForm):

	class Meta:
		model = AccountType
		fields = "__all__"
		widgets = {
			"name": forms.TextInput(attrs={
				'class': 'form-control',
			})
		}