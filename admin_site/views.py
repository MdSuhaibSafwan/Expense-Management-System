from django.shortcuts import render
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


class AdminPasswordResetView(PasswordResetView):
    template_name = "registration/custom_password_reset_form.html"


class AdminPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/custom_password_reset_done.html"


class AdminPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/custom_password_reset_confirm.html"

