from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BankAccount(models.Model):
    name = models.CharField(max_length=1000)
    account_no = models.IntegerField()
    balance = models.FloatField(default=0)
    account_type = models.CharField(max_length=3)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# class CashCheckout(models.Model):
#     title = models.CharField(max_length=100)
#     bank = models.ForeignKey(RegisteredBank, on_delete=models.SET_NULL, null=True)
#     cash = models.FloatField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"<Checkout: {self.bank}>"
