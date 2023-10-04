from django.db import models
from django.contrib.auth import get_user_model
from bank.models import BankCashout

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ExpenseManager(models.Manager):
    pass


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    bank_cashout = models.ForeignKey(BankCashout, on_delete=models.SET_NULL, null=True, related_name="expenses")
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    cost = models.FloatField()
    files = models.FileField(upload_to="expense/", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects = ExpenseManager()

    def __str__(self):
        return str(self.id)
    
    def total_cost(self):
        return self.cost

    def bank_cashout_title(self):
        return self.bank_cashout.title
