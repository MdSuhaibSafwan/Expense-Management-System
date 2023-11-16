import secrets
from django.db import models
from django.contrib.auth import get_user_model
from account.models import Account
from lib.models import BaseModel

User = get_user_model()


class CategoryManager(models.Manager):
    
    def get_total_expense_set_by_queryset(self, queryset=None):
        name_list = []
        total_expense_list = []
        if not queryset:
            queryset = self.all()
        for category in queryset:
            total = sum(list(category.expense_set.all().values_list("cost", flat=True)))
            if total > 0:
                total_expense_list.append(total)
                name_list.append(category.name)

        return name_list, total_expense_list


class Category(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    objects = CategoryManager()

    def __str__(self):
        return self.name


class ExpenseManager(models.Manager):

    def get_payments_for_a_year_monthly(self, year_number):
        qs = self.filter(date_created__year=year_number)
        month_number_lst = []
        monthly_cost = []
        for month_number in range(1, 12+1):
            temp_qs = qs.filter(date_created__month=month_number)
            if temp_qs.exists():
                month_number_lst.append(month_number)
                monthly_cost.append(sum(list(temp_qs.values_list("cost", flat=True))))

        return month_number_lst, monthly_cost


class Expense(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, )
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    cost = models.FloatField()
    files = models.FileField(upload_to="expense/", null=True, blank=True)
    transaction_code = models.CharField(max_length=64, unique=True, default=secrets.token_hex)

    objects = ExpenseManager()

    def __str__(self):
        return str(self.id)
    
    def total_cost(self):
        return self.cost