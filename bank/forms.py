from django import forms
from .models import BankCashout


class BankCashoutForm(forms.ModelForm):

    class Meta:
        model = BankCashout
        fields = "__all__"

    def clean_cash(self):
        cash = self.cleaned_data.get("cash")
        bank = self.cleaned_data.get("bank")
        try:
            change_view = self.change_view
        except Exception as e:
            change_view = False
        remaining_total = bank.get_remaining_balance()
        if change_view:
            remaining_total += self.cashout_obj.cash

        if cash > remaining_total:
            raise forms.ValidationError("Not Sufficient Funds Available")

        return cash
