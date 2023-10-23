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
			path("setup-2fa/", self.admin_view(TwoFactorAuthSetupView.as_view()), name="setup_2fa")
		] + urls_list

		return urls_list

	def two_fa_decorator(self, view):
		def wrapper(request, *args, **kwargs):
			user = request.user
			if not user.is_authenticated:
				return redirect("/login/")

			if user.has_valid_2fa():
				return view(request, *args, **kwargs)

			return redirect("/setup-2fa/")

		return wrapper

site = AdminSiteConfig(name="Expense Management")
