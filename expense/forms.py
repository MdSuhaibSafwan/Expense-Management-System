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
        self.validate_changed_data_according_to_user_type()
        return data
    
    def validate_changed_data_according_to_user_type(self):
        a = {
            "is_approved": "is_checker",
            "is_completed": "is_maker",
        }
        for c_data in self.changed_data:
            try:
                user_type = a[c_data]
                print("User Type ", user_type)
                is_valid = getattr(self.user, user_type, False)
                if not is_valid:
                    raise forms.ValidationError("User not permitted to change")
            except IndexError:
                pass
        
        return True