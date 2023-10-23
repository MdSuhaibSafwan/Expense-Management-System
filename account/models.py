from django.db import models
from django.contrib.auth import get_user_model
from lib.models import BaseModel
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class AccountType(BaseModel):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class AccountManager(models.Manager):
	pass



class Account(BaseModel):
	name = models.CharField(max_length=200)
	account_no = models.CharField(max_length=100, unique=True)
	routing_no = models.CharField(max_length=200, null=True, blank=True)
	opening_balance = models.FloatField(default=0)
	date_created = models.DateTimeField(default=timezone.now)
	account_type = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)

	objects = AccountManager()

	def __str__(self):
		return self.name

	def get_current_balance(self):
		return self.opening_balance

	def get_latest_outgoing_fund_transfer(self):
		obj = self.fund_transfer_from.order_by("-date_created").first()
		if obj is None:
			return None

		return obj

	def get_latest_incoming_fund_transfer(self):
		obj = self.fund_transfer_to.order_by("-date_created").first()
		if obj is None:
			return None

		return obj

	def get_latest_approved_outgoing_fund_transfer(self):
		qs = self.fund_transfer_from.filter(Q(approval_response__is_approved=True)).order_by("-date_created")
		return qs.last()


	def get_latest_approved_incoming_fund_transfer(self):
		qs = self.fund_transfer_to.filter(Q(approval_response__is_approved=True)).order_by("-date_created")
		return qs.last()


class FundTransfer(BaseModel):
	amount = models.FloatField()
	description = models.TextField()
	checker_assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fund_transfer_checked")
	from_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name="fund_transfer_from")
	to_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, related_name="fund_transfer_to")

	def __str__(self):
		return str(self.id)

	def save(self, *args, **kwargs):
		if self.from_account == self.to_account:
			raise ValueError("Account cannot transfer among itself")

		return super().save(*args, **kwargs)

	def is_approved(self):
		try:
			obj = self.approved_obj
		except Exception:
			obj = self.get_approval_response()

		if obj is None:
			return False

		return obj.is_approved

	def approved(self):
		obj = self.get_approval_response()
		if obj is None:
			return None
		self.approved_obj = obj
		return str(obj.user)

	def get_approval_response(self):
		try:
			obj = self.approval_response
		except ObjectDoesNotExist:
			return None

		return obj

	def is_checked(self):
		try:
			obj = self.checked_obj
		except Exception as e:
			obj = self.get_checking_response()
		
		if obj is None:
			return False	

		return obj.is_checked

	def checked(self):
		obj = self.get_checking_response()
		if obj is None:
			return None	

		self.checked_obj = obj
		return str(obj.user)

	def get_checking_response(self):
		try:
			obj = self.checked_response
		except ObjectDoesNotExist:
			return None

		return obj


class FundCheck(BaseModel):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	description = models.TextField()
	is_checked = models.BooleanField()
	fund_transfer = models.OneToOneField(FundTransfer, on_delete=models.PROTECT, related_name="checked_response")
	approver_assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="fund_checked")
	is_2fa_verified = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)


class FundApprove(BaseModel):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	description = models.TextField()
	is_approved = models.BooleanField()
	fund_transfer = models.OneToOneField(FundTransfer, on_delete=models.PROTECT, related_name="approval_response")
	fund_check = models.OneToOneField(FundCheck, on_delete=models.PROTECT)
	is_2fa_verified = models.BooleanField(default=False)

	def __str__(self):
		return str(self.id)
