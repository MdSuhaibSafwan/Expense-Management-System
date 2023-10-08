from django.db import models
from django.contrib.auth import get_user_model
from lib.models import BaseModel
from django.utils import timezone

User = get_user_model()


class AccountType(BaseModel):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Account(BaseModel):
	name = models.CharField(max_length=200)
	account_no = models.CharField(max_length=100, unique=True)
	routing_no = models.CharField(max_length=200, null=True, blank=True)
	opening_balance = models.FloatField(default=0)
	date_created = models.DateTimeField(default=timezone.now)
	account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.name


class FundTransfer(BaseModel):
	amount = models.FloatField()
	description = models.TextField()
	from_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="accounts_from")
	to_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="accounts_to")

	def __str__(self):
		return str(self.id)

	def is_approved(self):
		pass

	def get_approve_response(self):
		pass

	def is_checked(self):
		pass

	def get_check_response(self):
		pass

class FundApproveResponse(BaseModel):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	description = models.TextField()
	is_approved = models.BooleanField()
	fund_transfer = models.ForeignKey(FundTransfer, on_delete=models.CASCADE, )

	def __str__(self):
		return str(self.id)


class FundCheckResponse(BaseModel):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	description = models.TextField()
	is_checked = models.BooleanField()
	fund_transfer = models.ForeignKey(FundTransfer, on_delete=models.CASCADE, )

	def __str__(self):
		return str(self.id)
