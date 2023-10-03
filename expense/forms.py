from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Expense
from bank.models import BankAccount, BankCashout


class ExpenseAdminForm(ModelForm):

    class Meta:
        model = Expense
        fields = "__all__"

    def clean(self):
        data = super().clean()
        changed_data = self.changed_data
        return data
    
    def clean_cost(self):
        cost = self.cleaned_data.get("cost")
        bank_cashout_obj = BankCashout.objects.get_latest_approved_object()
        remaining_total = bank_cashout_obj.cash - sum(list(bank_cashout_obj.expenses.all().values_list("cost", flat=True)))
        if self.should_add_cost:
            remaining_total += self.added_cost
            
        if cost > remaining_total:
            raise forms.ValidationError("Not sufficient balance")
        
        return cost

    def validate_changed_data(self):
        data = {
            "is_author": "category",
            "is_author": "title",
            "is_author": "cost",
            "is_checker": "is_approved",
            "is_maker": "is_completed",
        }
        user_type = self.user.get_user_type()
        


class ExpenseAdminReportForm(forms.Form):
    error_text = "Please Provide date correctly"

    date1 = forms.DateField()
    date2 = forms.DateField()

    def clean(self):
        data =  super().clean()
        date1, date2 = data.get("date1"), data.get("date2")
        if (date1 is None) or (date2 is None):
            self.error_text = "Please provide date"
            raise forms.ValidationError("Please provide date")
        if date1 == date2:
            raise forms.ValidationError("Date mismatched")
        
        if date1 > date2:
            raise forms.ValidationError("date2 cannot be more than date1")
        
        return data

