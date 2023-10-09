from django.dispatch import receiver
from expense.dispatch import expense_created_signal
from .dispatch import bank_cashout_approved
from .utils import create_cash_history


@receiver(signal=expense_created_signal)
def create_cash_history_for_expense(sender, instance, **kwargs):
	create_cash_history(instance)

@receiver(signal=bank_cashout_approved)
def create_cash_history_for_bank_account_cashout(sender, instance, **kwargs):
	create_cash_history(instance)
