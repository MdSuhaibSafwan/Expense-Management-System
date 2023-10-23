from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from .models import FundTransfer
from .forms import FundCheckForm, FundApproveForm
from django.contrib import messages


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
			return redirect("/")
		messages.error(request, form.errors)

	context["form"] = form

	return render(request, "admin/account/fund_check_approve.html", context)


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
			return redirect("/")
			
		messages.error(request, form.errors)

	context["form"] = form

	return render(request, "admin/account/fund_check_approve.html", context)


