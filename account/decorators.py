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
		try:
			ft_obj = FundTransfer.objects.get(pk=kwargs.get("pk"))
		except ObjectDoesNotExist as e:
			messages.error(request, e)
			return redirect("/")

		fc_obj = ft_obj.get_checking_response()
		if not fc_obj:
			messages.error(request, "Fund Checked Object is not found")
			return redirect("/")

		if not fc_obj.is_checked:
			messages.error(request, "Fund check has been declined")
			return redirect("/")

		if not fc_obj.is_2fa_verified:
			messages.error(request, "Fund Check is not verified correctly")
			return redirect("/")

		kwargs["ft_approved_obj"] = ft_obj.get_approval_response()
		kwargs["fc_obj"] = fc_obj
		kwargs["ft_obj"] = ft_obj

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
			if not ft_checked_obj.is_2fa_verified:
				messages.warning(request, "please verify 2FA to update or keep for approval")
				return redirect(f"/account/fundtransfer/{kwargs.get('pk')}/check/verify-otp/")

		kwargs["ft_checked_obj"] = ft_checked_obj

		return function(request, *args, **kwargs)

	return wrapper


def redirect_to_home_if_already_verified(function, to_url="/"):

	def wrapper(request, *args, **kwargs):
		try:
			obj = FundTransfer.objects.get(pk=kwargs.get("pk"))
		except ObjectDoesNotExist as e:
			messages.error(request, e)
			return redirect(to_url)

		fc_obj = obj.get_checking_response()
		if fc_obj:
			if fc_obj.is_2fa_verified:
				messages.success(request, "Already Verified")
				return redirect(to_url)

		kwargs["fc_obj"] = fc_obj

		return function(request, *args, **kwargs)
	return wrapper