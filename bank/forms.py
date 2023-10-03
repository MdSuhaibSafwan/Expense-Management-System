from django import forms
from .models import BankCashout


class BankCashoutForm(forms.ModelForm):

    class Meta:
        model = BankCashout
        fields = "__all__"
