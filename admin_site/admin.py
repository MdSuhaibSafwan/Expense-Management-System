from django.contrib import admin


class AdminSiteConfig(admin.AdminSite):
	site_header = "Expense Management"


site = AdminSiteConfig(name="Expense Management")
