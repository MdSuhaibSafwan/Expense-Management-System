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

	def get_current_balance(self):
		return self.opening_balance


class FundTransfer(BaseModel):
	amount = models.FloatField()
	description = models.TextField()
	from_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="accounts_from")
	to_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="accounts_to")

	def __str__(self):
		return str(self.id)

	def save(self, *args, **kwargs):
		if self.from_account == self.to_account:
			raise ValueError("Account cannot transfer among itself")

		return super().save(*args, **kwargs)

	def is_approved(self):
		obj = self.get_approval_response()
		if obj is None:
			return False

		return obj.is_approved

	def get_approval_response(self):
		try:
			obj = self.approval_response
		except ObjectDoesNotExist:
			return None

		return obj

	def is_checked(self):
		obj = self.get_checking_response()
		if obj is None:
			return False

		return obj.is_checked

	def get_checking_response(self):
		try:
			obj = self.checked_response
		except ObjectDoesNotExist:
			return None

		return obj


class FundApproveResponse(BaseModel):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	description = models.TextField()
	is_approved = models.BooleanField()
	fund_transfer = models.OneToOneField(FundTransfer, on_delete=models.CASCADE, related_name="approval_response")

	def __str__(self):
		return str(self.id)


class FundCheckResponse(BaseModel):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	description = models.TextField()
	is_checked = models.BooleanField()
	fund_transfer = models.OneToOneField(FundTransfer, on_delete=models.CASCADE, related_name="checked_response")

	def __str__(self):
		return str(self.id)
