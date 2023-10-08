from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
	list_display = ["id", ]

