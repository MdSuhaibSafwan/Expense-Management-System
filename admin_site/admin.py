from django.contrib import admin
from django.contrib.admin import *
from user.views import TwoFactorAuthSetupView
from django.urls import path
from django.views.decorators.common import no_append_slash
from django.urls.resolvers import URLPattern, URLResolver


class AdminSiteConfig(admin.AdminSite):
	site_header = "Expense Management"

	def get_urls(self, *args, **kwargs):
		previous_urls = super().get_urls(*args, **kwargs)
		urls = [
			path("setup-2fa/", self.admin_view(TwoFactorAuthSetupView.as_view()), name="setup_2fa")
		] + previous_urls

		urls_list = []
		for url in urls:
			if isinstance(url, URLPattern):
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

		return urls_list

	def two_fa_decorator(self, view):
		print("Inside decorator ", view)
		return view


site = AdminSiteConfig(name="Expense Management")
