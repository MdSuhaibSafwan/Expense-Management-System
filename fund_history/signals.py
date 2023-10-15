from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.contrib.contenttypes.models import ContentType
from account.dispatch import fund_transfer_approved
from account.models import FundTransfer
from expense.models import Expense
from .models import FundHistory


@receiver(signal=post_save, sender=Expense)
def add_an_instruction_to_journal_for_expense(sender, instance, created, **kwargs):
	if not created:
		return None

	content_type = ContentType.objects.get_for_model(Expense)
	title = "An expense"
	description = title
	fh_obj = FundHistory(object_id=instance.id, content_type=content_type, amount=instance.cost,
		title=title, description=description)
	fh_obj.transaction_code = instance.id
	fh_obj.save()


@receiver(signal=fund_transfer_approved)
def add_an_instruction_to_journal_for_account_fund_transfer(sender, instance, **kwargs):
	content_type = ContentType.objects.get_for_model(instance.__class__)
	title = "Fund Transfer between accounts"
	if not instance.from_account:
		title = "Balance add on account"
	description = title
	fh_obj = FundHistory(object_id=instance.id, content_type=content_type, amount=instance.amount,
			title=title, description=description)
	fh_obj.transaction_code = instance.id
	fh_obj.save()
