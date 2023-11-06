from django import forms
from django.forms import ModelForm
from .models import Expense


CLASS_NAME = "form-control"

class ExpenseAdminForm(ModelForm):

    class Meta:
        model = Expense
        exclude = ["user", ]
        widgets = {
            'description': forms.Textarea(attrs={'class': CLASS_NAME})
        }

    def clean(self):
        data = super().clean()
        return data

    def validate_changed_data(self):
        data = {
            "is_author": "category",
            "is_author": "title",
            "is_author": "cost",
            "is_checker": "is_approved",
            "is_maker": "is_completed",
        }
        user_type = self.user.get_user_type()

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.user = self.user
        obj.save()
        return obj


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

