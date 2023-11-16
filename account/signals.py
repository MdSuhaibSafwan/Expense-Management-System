from django.db.models.signals import post_save, pre_save
from .models import Account, FundTransfer, FundCheck, FundApprove
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .dispatch import fund_transfer_approved


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
		if instance.is_approved:
			fund_transfer_approved.send(sender=FundTransfer.__class__, instance=instance.fund_transfer)
	
		return True

	return False


@receiver(signal=fund_transfer_approved)
def calculate_account_balance_between_accounts_if_related(sender, instance, **kwargs):
	""" REDUCE AND ADD ACCOUNT OPENING BALANCE """
	
	from_account = instance.from_account
	to_account = instance.to_account
	if from_account:
		from_account.opening_balance -= instance.amount
		from_account.save()

	to_account.opening_balance += instance.amount
	to_account.save()