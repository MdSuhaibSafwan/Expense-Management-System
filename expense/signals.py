import django
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from .models import Expense


@receiver(signal=post_save, sender=Expense)
def deduct_account_balance(sender, instance, created, **kwargs):
	if not created:
		return None

	account = instance.account
	account.opening_balance -= instance.cost
	account.save()


@receiver(signal=pre_delete, sender=Expense)
def restore_account_balace_for_that_expense(sender, instance, **kwargs):
	account = instance.account
	account.opening_balance += instance.cost
	account.save()	
