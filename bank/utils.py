from django.contrib.contenttypes.models import ContentType
from .models import CashHistory


def create_cash_history(instance):
	app_label = instance._meta.app_label
	model_name = instance.__class__.__name__
	try:
		amount = instance.amount
	except AttributeError:
		amount = instance.cash
	except AttributeError:
		amount = instance.cost
	
	content_type, created = ContentType.objects.get_or_create(app_label=app_label, model=model_name.lower())
	ch_obj = CashHistory.objects.create(content_type=content_type, object_id=instance.id, 
			content_object=instance, amount=amount)

	return ch_obj