from django.db import models
from django.contrib.auth import get_user_model
from account.models import Account
from lib.models import BaseModel

User = get_user_model()


class Category(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class ExpenseManager(models.Manager):
    pass


class Expense(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, )
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    cost = models.FloatField()
    files = models.FileField(upload_to="expense/", null=True, blank=True)

    objects = ExpenseManager()

    def __str__(self):
        return str(self.id)
    
    def total_cost(self):
        return self.cost
