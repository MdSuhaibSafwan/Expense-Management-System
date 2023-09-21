from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Expense


class ExpenseAdminForm(ModelForm):
    # some works need to be done

    class Meta:
        model = Expense
        fields = "__all__"

    def clean(self):
        data = super().clean()
        return data


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

