from django.contrib import messages
from django.shortcuts import redirect


def user_checker_required(function=None, to_url="/"):

	def wrapper(request, *args, **kwargs):
		if not request.user.is_checker:
			messages.error(request, "User is not a checker")
			return redirect("/")
		
		return function(request, *args, **kwargs)

	return wrapper


def user_approver_required(function=None, to_url="/"):

	def wrapper(request, *args, **kwargs):
		if not request.user.is_approver:
			messages.error(request, "User is not an approver")
			return redirect("/")

		return function(request, *args, **kwargs)

	return wrapper

