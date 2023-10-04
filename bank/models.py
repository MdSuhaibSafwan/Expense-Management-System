from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BankAccount(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ["PT", "Pretty Cash Account"],
        ["MW", "MERCHANT ACCOUNT"],
        ["OT", "OTHERS"],
    ]
    name = models.CharField(max_length=1000)
    account_no = models.IntegerField(unique=True)
    balance = models.FloatField(default=0)
    account_type = models.CharField(max_length=3, choices=ACCOUNT_TYPE_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_total_cashouts(self):
        cashouts = self.cashouts.all()
        return sum(list(cashouts.values_list("cash", flat=True)))

    def get_remaining_balance(self):
        expenditure = self.get_total_cashouts()
        return (self.balance - expenditure)

    def open_balance(self):
        return self.get_remaining_balance()


class BankCashoutManager(models.Manager):

    def get_latest_approved_queryset(self):
        qs = self.filter(is_approved=True, is_completed=True).order_by("-date_created")
        return qs
    
    def get_latest_approved_object(self):
        qs = self.get_latest_approved_queryset()
        obj = qs.first()
        return obj


class BankCashout(models.Model):
    title = models.CharField(max_length=100)
    bank = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, related_name="cashouts")
    cash = models.FloatField()
    is_approved = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    objects = BankCashoutManager()

    def __str__(self):
        return f"<Checkout: {self.bank} {self.id}>"
    
    def is_finished(self):
        return self.get_remaining_balance() <= 0
    
    def get_total_expense(self):
        return sum(list(self.expenses.all().values_list("cost", flat=True)))
    
    def get_remaining_balance(self):
        total_expense = self.get_total_expense()
        return self.cash - total_expense
