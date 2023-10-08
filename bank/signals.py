from django.dispatch import receiver
from expense.dispatch import expense_created_signal
from django.contrib.contenttypes.models import ContentType
from .models import CashHistory


@receiver(signal=expense_created_signal)
def create_cash_history_for_expense(sender, expense, **kwargs):
	app_label = expense._meta.app_label
	model_name = expense.__class__.__name__
	content_type, created = ContentType.objects.get_or_create(app_label=app_label, model=model_name.lower())
	ch_obj = CashHistory.objects.create(content_type=content_type, object_id=expense.id, 
			content_object=expense, amount=expense.cost)

	return ch_obj
