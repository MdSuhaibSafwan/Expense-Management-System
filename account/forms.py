from django import forms
from .models import FundTransfer


class FundTransferForm(forms.ModelForm):

	class Meta:
		model = FundTransfer
		fields = "__all__"

	def clean(self):
		data = super().clean()
		from_account = data.get("from_account")
		to_account = data.get("to_account")
		if from_account == to_account:
			raise forms.ValidationError("Accounts Cannot transfer among themselves")

		amount = data.get("amount")
		if from_account.get_current_balance() < amount:
			raise forms.ValidationError("Insufficient Balance")

		self.validate_from_account(data)

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
		if checker_resp_obj is None:
			self.add_error("from_account", "Please provide a check to fund transaction to apply again from this account")

		return True

	def validate_approval_response(self, fund_transfer_obj):
		approval_response_obj = fund_transfer_obj.get_approval_response()
		if approval_response_obj is None:
			self.add_error("from_account", "Please approve previous fund transaction to apply again from this account")

		return True

