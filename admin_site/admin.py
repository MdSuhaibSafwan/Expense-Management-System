from django.contrib import admin
from django.contrib.admin import *
from user.views import TwoFactorAuthSetupView
# from account.views import FundTransferCheckOtpDetailView
from django.urls import path, include
from django.views.decorators.common import no_append_slash
from django.urls.resolvers import URLPattern, URLResolver
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from expense.models import Category, Expense
from django.contrib.auth import get_user_model
from django.utils import timezone
from account.views import account_report_view

User = get_user_model()


class AdminSiteConfig(admin.AdminSite):
	site_header = "Expense Management"

	def get_all_urls(self, *args, **kwargs):
		urls = super().get_urls(*args, **kwargs)
		urls = [
			path("account/fundtransfer/<int:pk>/", include("account.urls"), )
		] + urls

		return urls

	def get_urls(self, *args, **kwargs):
		urls = self.get_all_urls(*args, **kwargs)
		urls_list = []
		for url in urls:
			if isinstance(url, URLPattern):
				if (url.name == "login") or (url.name == "logout"):
					urls_list.append(url)
					continue

				urls_list.append(
					URLPattern(
						pattern=url.pattern, 
						callback=self.two_fa_decorator(url.callback),
						default_args=url.default_args,
						name=url.name
					)
				)
			elif isinstance(url, URLResolver):
				urls_list.append(
					URLResolver(
				        pattern = url.pattern,
				        urlconf_name = url.urlconf_name,
				        namespace = url.namespace,
				        app_name = url.app_name,
					)
				)

		urls_list = [
			path("setup-2fa/", self.admin_view(TwoFactorAuthSetupView.as_view()), name="setup_2fa"),
			path("account/account/account-report/", self.report_for_account_view, ),
		] + urls_list

		return urls_list

	def report_for_account_view(self, request):
		return account_report_view(request)

	def two_fa_decorator(self, view):
		def wrapper(request, *args, **kwargs):
			user = request.user
			if not user.is_authenticated:
				return redirect("/login/")

			if user.has_valid_2fa():
				return view(request, *args, **kwargs)

			return redirect("/setup-2fa/")

		return wrapper

	def index(self, request, extra_content=None):
		if extra_content == None:
			extra_content = {}

		name_list, expense_list = Category.objects.get_total_expense_set_by_queryset()
		extra_content["name_list"] = list(name_list)
		extra_content["expense_list"] = expense_list
		extra_content["expense_months"], extra_content["expense_costs"] = Expense.objects.get_payments_for_a_year_monthly(2023)
		exp_qs = Expense.objects.all()
		extra_content["total_expense"] = sum(list(exp_qs.values_list("cost", flat=True)))
		extra_content["this_month_expense"] = sum(list(exp_qs.filter(date_created__month=timezone.now().month).values_list("cost", flat=True)))
		extra_content["this_year_expense"] = sum(list(exp_qs.filter(date_created__year=timezone.now().year).values_list("cost", flat=True)))
		extra_content["total_users"] = User.objects.all().count()		
		return super().index(request, extra_content)

site = AdminSiteConfig(name="Expense Management")
