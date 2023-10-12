import django
from .models import FundTransfer, FundApprove, FundCheck
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.exceptions import ObjectDoesNotExist

fund_transfer_approved = django.dispatch.Signal()
fund_transfer_is_checked = django.dispatch.Signal()


@receiver(signal=post_save, sender=FundApprove)
def send_signal_if_fund_transfer_approved(sender, instance, created, **kwargs):
	if not created:
		return None

	fund_transfer_approved.send(sender=FundTransfer.__class__, instance=instance.fund_transfer)


@receiver(signal=post_save, sender=FundCheck)
def send_signal_if_fund_transfer_is_checked(sender, instance, created, **kwargs):
	if not created:
		return None

	fund_transfer_is_checked.send(sender=FundCheck.__class__, instance=instance.fund_transfer)
