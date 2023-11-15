from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .models import FundTransfer, FundCheck, FundApprove
from .forms import FundCheckForm, FundApproveForm
from django.contrib import messages
from .decorators import (user_checker_required, user_approver_required, redirect_to_home_if_already_verified,
		fund_transfer_checked_required, redirect_to_verification_if_fund_transfer_checked)
from user.models import User2FAAuth


@user_checker_required
@redirect_to_verification_if_fund_transfer_checked
def fund_transfer_check_admin_view(request, pk, ft_checked_obj=None):
	ft_obj = get_object_or_404(FundTransfer, pk=pk)
	if not ft_checked_obj:
		ft_checked_obj = ft_obj.get_checking_response()
	
	form = FundCheckForm()
	context = {}
	if ft_checked_obj:
		form = FundCheckForm(instance=ft_checked_obj)

	if request.method == "POST":
		form = FundCheckForm(request.POST)
		if ft_checked_obj:
			form.instance = ft_checked_obj

		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			obj.fund_transfer = ft_obj
			obj.save()
			messages.success(request, "Verify your otp")
			return redirect(f"/account/fundtransfer/{ft_obj.pk}/check/verify-otp/")
		messages.error(request, form.errors)

	context["form"] = form

	return redirect(f"/account/fundtransfer/{ft_obj.pk}/")


@user_approver_required
@fund_transfer_checked_required
def fund_transfer_approve_admin_view(request, pk, ft_obj=None, fc_obj=None, ft_approved_obj=None):
	if not ft_obj:
		ft_obj = get_object_or_404(FundTransfer, pk=pk)
	
	if not ft_approved_obj:
		ft_approved_obj = ft_obj.get_approval_response()
	
	if not fc_obj:
		fc_obj = ft_obj.get_checking_response()
	
	form = FundApproveForm()
	
	context = {}
	
	if ft_approved_obj:
		form = FundApproveForm(instance=ft_approved_obj)

	if request.method == "POST":
		form = FundApproveForm(request.POST)
		form.user = request.user
		form.ft_obj = ft_obj
		form.fc_obj = fc_obj

		if ft_approved_obj:
			form.instance = ft_approved_obj

		if form.is_valid():
			messages.success(request, "Verify your otp")
			obj = form.save(commit=False)
			obj.user = request.user
			obj.fund_transfer = ft_obj
			obj.fund_check = fc_obj
			obj.save()
			return redirect(f"/account/fundtransfer/{ft_obj.pk}/approve/verify-otp/")

		messages.error(request, "Please Check the following issues")

	context["form"] = form

	return redirect(f"/account/fundtransfer/{ft_obj.pk}/")


@user_checker_required
@redirect_to_home_if_already_verified
def verify_otp_for_fund_check(request, pk, fc_obj=None):
	context = {}
	ft_obj = get_object_or_404(FundTransfer, pk=pk)
	
	if not fc_obj:
		fc_obj = ft_obj.get_checking_response()
	
	if fc_obj is None:
		return redirect("/")
	user_2fa_obj, created = User2FAAuth.objects.get_or_create(user=request.user)

	if request.method == 'POST':
		otp = request.POST.get("otp", None)
		is_valid = user_2fa_obj.is_token_valid(otp)
		if is_valid:
			fc_obj.is_2fa_verified = True
			fc_obj.save()
			messages.success(request, "Fund has been checked")
			return redirect("/")
	
		messages.error(request, "Invalid token provided")

	return render(request, "admin/two_fa/setup.html", context)


@user_approver_required
def verify_otp_for_fund_approve(request, pk):
	context = {}
	ft_obj = get_object_or_404(FundTransfer, pk=pk)
	fa_obj = ft_obj.get_approval_response()
	if fa_obj is None:
		messages.error(request, "Invalid url Provided")
		return redirect("/")

	user_2fa_obj, created = User2FAAuth.objects.get_or_create(user=request.user)

	if request.method == 'POST':
		otp = request.POST.get("otp", None)
		is_valid = user_2fa_obj.is_token_valid(otp)
		if is_valid:
			fa_obj.is_2fa_verified = True
			fa_obj.save()
			messages.success(request, "Fund has been approved")
			return redirect("/")
	
		messages.error(request, "Invalid token provided")

	return render(request, "admin/two_fa/setup.html", context)



