from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .models import FundTransfer, FundCheck, FundApprove
from .forms import FundCheckForm, FundApproveForm
from django.contrib import messages
from .decorators import user_checker_required, user_approver_required
from user.models import User2FAAuth


@user_checker_required
def fund_transfer_check_admin_view(request, pk):
	ft_obj = get_object_or_404(FundTransfer, pk=pk)
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

	return render(request, "admin/account/fund_check_approve.html", context)


@user_approver_required
def fund_transfer_approve_admin_view(request, pk):
	ft_obj = get_object_or_404(FundTransfer, pk=pk)
	ft_approved_obj = ft_obj.get_approval_response()
	form = FundApproveForm()
	context = {}
	if ft_approved_obj:
		form = FundApproveForm(instance=ft_approved_obj)

	if request.method == "POST":
		form = FundApproveForm(request.POST)
		if ft_approved_obj:
			form.instance = ft_approved_obj

		if form.is_valid():
			messages.success(request, "Verify your otp")
			obj = form.save(commit=False)
			obj.user = request.user
			obj.fund_transfer = ft_obj
			obj.fund_check = ft_obj.get_checking_response()
			obj.save()
			return redirect(f"/account/fundtransfer/{ft_obj.pk}/approve/verify-otp/")

		messages.error(request, "Please Check the following issues")

	context["form"] = form

	return render(request, "admin/account/fund_check_approve.html", context)


def verify_otp_for_fund_check(request, pk):
	context = {}
	ft_obj = get_object_or_404(FundTransfer, pk=pk)
	fc_obj = ft_obj.get_checking_response()
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


def verify_otp_for_fund_approve(request, pk):
	context = {}
	ft_obj = get_object_or_404(FundTransfer, pk=pk)
	fa_obj = ft_obj.get_approval_response()

	user_2fa_obj, created = User2FAAuth.objects.get_or_create(user=request.user)

	if request.method == 'POST':
		otp = request.POST.get("otp", None)
		is_valid = user_2fa_obj.is_token_valid(otp)
		if is_valid:
			fa_obj.is_2fa_verified = True
			fa_obj.save()
			messages.success(request, "Fund has been approved")
			return redirect(f"/account/fundtransfer/{ft_obj.pk}/approve/verify-otp/")
	
		messages.error(request, "Invalid token provided")

	return render(request, "admin/two_fa/setup.html", context)

