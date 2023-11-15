from django import forms
from django.forms import ModelForm
from .models import Expense, Category


class CategoryAdminForm(ModelForm):

    class Meta:
        model = Category
        fields = "__all__"

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),

            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class ExpenseAdminForm(ModelForm):

    class Meta:
        model = Expense
        exclude = ["user", "transaction_code"]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),

            'account': forms.Select(attrs={
                'class': 'form-control',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            
            'files': forms.FileInput(attrs={
                'class': 'form-control',
            })
        }

    def clean(self):
        data = super().clean()

        account = data.get("account", None)
        cost = data.get("cost", None)
        if not account:
            return self.add_error("account", "Provide an Account")

        if cost > account.opening_balance:
            return self.add_error("cost", "Insufficient Balance")

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

