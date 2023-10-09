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

		return data

	def clean_amount(self):
		amount = self.cleaned_data.get("amount")
		from_account = self.cleaned_data.get("from_account")
		if from_account.get_current_balance() < amount:
			raise forms.ValidationError("Insufficient Balance")

		return amount
