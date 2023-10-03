from django.contrib import admin
from .models import BankAccount


class BankAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "balance"]

admin.site.register(BankAccount, BankAdmin)
