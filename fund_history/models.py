from django.db import models
from lib.models import BaseModel
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class FundHistory(BaseModel):
	object_id = models.PositiveIntegerField()
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, )
	content_object = GenericForeignKey('content_type', 'object_id')
	transaction_code = models.SlugField(null=True)

	class Meta:
		unique_together = [["content_type", "object_id"], ]
