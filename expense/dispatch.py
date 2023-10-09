import django
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Expense

expense_created_signal = django.dispatch.Signal()


@receiver(signal=post_save, sender=Expense)
def send_signal_expense_created(sender, instance, created, **kwargs):
	if created:
		expense_created_signal.send(sender=Expense.__class__, instance=instance)
