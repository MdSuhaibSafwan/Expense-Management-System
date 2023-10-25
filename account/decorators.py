from django.contrib import messages
from django.shortcuts import redirect
from .models import FundTransfer, FundCheck, FundApprove


def user_checker_required(function=None, to_url="/"):

	def wrapper(request, *args, **kwargs):
		if not request.user.is_checker:
			messages.error(request, "User is not a checker")
			return redirect(to_url)

		return function(request, *args, **kwargs)

	return wrapper


def user_approver_required(function=None, to_url="/"):

	def wrapper(request, *args, **kwargs):
		if not request.user.is_approver:
			messages.error(request, "User is not an approver")
			return redirect(to_url)

		return function(request, *args, **kwargs)

	return wrapper


def fund_transfer_checked_required(function, to_url="/"):

	def wrapper(request, *args, **kwargs):
		print(kwargs)

		return function(request, *args, **kwargs)

	return wrapper


def redirect_to_verification_if_fund_transfer_checked(function, to_url="/"):

	def wrapper(request, *args, **kwargs):
		try:
			obj = FundTransfer.objects.get(pk=kwargs.get("pk"))
		except ObjectDoesNotExist as e:
			messages.error(request, e)
			return redirect("/")

		ft_checked_obj = obj.get_checking_response()
		if ft_checked_obj:
			if ((ft_checked_obj.is_checked) and not ft_checked_obj.is_2fa_verified):
				return redirect(f"/account/fundtransfer/{kwargs.get('pk')}/check/verify-otp/")

		kwargs["ft_checked_obj"] = ft_checked_obj

		return function(request, *args, **kwargs)

	return wrapper
