from django.contrib import admin
from .models import BankAccount, BankCashout


class BankAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "balance"]


class BankCashoutAdmin(admin.ModelAdmin):
    list_display = ["id", "bank", "cash", "is_approved", "is_completed"]


admin.site.register(BankAccount, BankAdmin)
admin.site.register(BankCashout, BankCashoutAdmin)
