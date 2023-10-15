from django.db.models.signals import post_save
from .models import Account, FundTransfer
from django.dispatch import receiver
from .dispatch import fund_transfer_approved, fund_transfer_is_checked


@receiver(signal=fund_transfer_approved)
def add_and_reduce_account_balance(sender, instance: FundTransfer, **kwargs):
	from_account = instance.from_account
	to_account = instance.to_account
	amount = instance.amount
	to_account.opening_balance += amount
	if from_account is not None:
		from_account.opening_balance -= amount
		from_account.save()
	to_account.save()
