from django.urls import path, include
from admin_site import admin

urlpatterns = [
	path("admin/", admin.site.urls)    
]
