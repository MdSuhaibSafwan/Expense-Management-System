import uuid
from django.db import models

def create_hex_token():
	return uuid.uuid4()


class BaseModel(models.Model):
	id = models.UUIDField(primary_key=True, editable=False, unique=True, default=create_hex_token)
	date_created = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
