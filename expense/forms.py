from typing import Any
from django import forms
from django.forms import ModelForm
from .models import Expense


class ExpenseAdminForm(ModelForm):

    class Meta:
        model = Expense
        fields = "__all__"

    def clean(self):
        data = super().clean()
        return data


class ExpenseAdminReportForm(forms.Form):
    date1 = forms.DateField()
    date2 = forms.DateField()

    def clean(self):
        data =  super().clean()
        print("data ", data)
        return data

