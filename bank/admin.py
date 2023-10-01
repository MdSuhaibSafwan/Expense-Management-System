from django.contrib import admin
from .models import CashCheckout, RegisteredBank


class CashCheckoutAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "bank"]


class BankAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "open_balance"]


admin.site.register(CashCheckout, CashCheckoutAdmin)
admin.site.register(RegisteredBank, BankAdmin)
