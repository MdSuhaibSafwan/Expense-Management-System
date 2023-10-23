from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import User2FAAuth


class TwoFactorAuthSetupView(DetailView):
	template_name = "admin/two_fa/setup.html"
	context_object_name = "object"

	def get(self, request, *args, **kwargs):
		self.request = request
		qr_obj = self.get_object()
		context = self.get_context_data(object=qr_obj)
		return self.render_to_response(context)

	def get_queryset(self):
		return None

	def get_object(self):
		user = self.request.user
		qr_obj, created = User2FAAuth.objects.get_or_create(user=user)
		self.object = qr_obj
		return qr_obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["otp_secret"] = self.object.token
		context["qr_code"] = self.object.generate_qr_code()
		return context

	def post(self, request, *args, **kwargs):
		otp = self.request.POST.get("otp", None)
		qr_obj = self.get_object()
		is_valid = qr_obj.is_token_valid(otp)
		if not is_valid:
			context = self.get_context_data(object=qr_obj)
			return self.render_to_response(context)
		return redirect("/")
