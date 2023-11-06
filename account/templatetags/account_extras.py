from django import template

register = template.Library()


@register.simple_tag
def check_user_perm_for_model(user, app_name, model_name):
	return user.has_perm(f"{app_name}.change_{model_name}")

