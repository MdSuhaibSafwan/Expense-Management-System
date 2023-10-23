from django.contrib import admin
from django.contrib.admin import *
from user.views import TwoFactorAuthSetupView
from django.urls import path


class AdminSiteConfig(admin.AdminSite):
	site_header = "Expense Management"

	def get_urls(self, *args, **kwargs):
		previous_urls = super().get_urls(*args, **kwargs)
		urls = [
			path("setup-2fa/", self.admin_view(TwoFactorAuthSetupView.as_view()), name="setup_2fa")
		] + previous_urls
		return urls


site = AdminSiteConfig(name="Expense Management")
