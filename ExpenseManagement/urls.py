from django.urls import path, include
from admin_site import admin
from admin_site.views import AdminPasswordResetView, AdminPasswordResetDoneView, AdminPasswordResetConfirmView

urlpatterns = [
    path("auth/password_reset/", AdminPasswordResetView.as_view(), name="password_reset"),
    path("auth/password_reset/done/", AdminPasswordResetDoneView.as_view(), name="password_reset_done",),
    path("auth/reset/<uidb64>/<token>/", AdminPasswordResetConfirmView.as_view(), name="password_reset_confirm",),
	path("", admin.site.urls),
]
