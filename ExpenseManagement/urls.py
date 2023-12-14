from django.urls import path, include
from admin_site import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path("auth/password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("auth/password_reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done",),
    path("auth/reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm",),
    path("auth/reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete",),
	path("", admin.site.urls),
]
