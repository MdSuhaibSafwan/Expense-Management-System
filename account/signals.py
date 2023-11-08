from django.db.models.signals import post_save, pre_save
from .models import Account, FundTransfer, FundCheck, FundApprove
from django.dispatch import receiver
from .dispatch import fund_transfer_approved, fund_transfer_is_checked
from django.core.exceptions import ObjectDoesNotExist


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


@receiver(signal=pre_save, sender=FundCheck)
def complete_fund_check_if_2fa_verified(sender, instance, **kwargs):
	try:
		fc_obj = FundCheck.objects.get(id=instance.id)
	except ObjectDoesNotExist:
		return None

	if fc_obj.is_2fa_verified == instance.is_2fa_verified:
		return False

	if instance.is_2fa_verified == True:
		instance.is_completed = True		

	return True


@receiver(signal=pre_save, sender=FundApprove)
def complete_fund_approve_if_2fa_verified(sender, instance, **kwargs):
	try:
		fa_obj = FundApprove.objects.get(id=instance.id)
	except ObjectDoesNotExist:
		return None

	if fa_obj.is_2fa_verified == instance.is_2fa_verified:
		return False

	if instance.is_2fa_verified == True:
		instance.is_completed = True		

	return True
