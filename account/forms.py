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

		if not ((fund_transfer_obj.is_approved()) and (fund_transfer_obj.is_checked())):
			self.add_error("from_account", "Please Approve the previous Fund Transaction to apply again")

		return from_account



