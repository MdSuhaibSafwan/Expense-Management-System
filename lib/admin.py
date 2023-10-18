from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
	list_display = ["id", ]

	def add_view(self, request, *args, **kwargs):
		user = request.user
		print("Base Admin User ", user)

		return super().add_view(request, *args, **kwargs)


	def change_view(self, request, object_id, *args, **kwargs):
		user = request.user
		print("Base Admin User ", user)

		return super().change_view(request, object_id, *args, **kwargs)
