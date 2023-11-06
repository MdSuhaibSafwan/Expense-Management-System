from django import template

register = template.Library()


@register.simple_tag
def check_user_perm_for_model_to_add(user, app_name, model_name):
	return user.has_perm(f"{app_name}.add_{model_name}")



@register.simple_tag
def check_user_perm_for_model_to_change(user, app_name, model_name):
	return user.has_perm(f"{app_name}.change_{model_name}")


@register.simple_tag
def check_user_perm_for_model_to_delete(user, app_name, model_name):
	return user.has_perm(f"{app_name}.delete_{model_name}")
