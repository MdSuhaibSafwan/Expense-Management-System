from django.contrib import admin
from django.contrib.admin import *


class AdminSiteConfig(admin.AdminSite):
	site_header = "Expense Management"


site = AdminSiteConfig(name="Expense Management")
