import django
from .models import BankCashout
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

bank_cashout_approved = django.dispatch.Signal()

@receiver(signal=pre_save, sender=BankCashout)
def send_signal_when_bank_bill_approved(sender, instance, **kwargs):
	try:
		obj = BankCashout.objects.get(id=instance.id)
	except ObjectDoesNotExist:
		return False

	if obj.is_completed == instance.is_completed:
		return False
	
	if not instance.is_completed:
		return False

	bank_cashout_approved.send(sender=BankCashout.__class__, instance=instance)