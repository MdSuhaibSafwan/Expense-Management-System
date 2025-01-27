import re
from django import template
from ..utils import get_fields_from_cl

register = template.Library()

MONTH_DICT = {
	"1": "January",
	"2": "February",
	"3": "March",
	"4": "April",
	"5": "May",
	"6": "June",
	"7": "July",
	"8": "August",
	"9": "September",
	"10": "October",
	"11": "November",
	"12": "December",
}

@register.simple_tag
def check_user_perm_for_model_to_add(user, app_name, model_name):
	return user.has_perm(f"{app_name}.add_{model_name}")

@register.simple_tag
def check_user_perm_for_model_to_change(user, app_name, model_name):
	return user.has_perm(f"{app_name}.change_{model_name}")


@register.simple_tag
def check_user_perm_for_model_to_delete(user, app_name, model_name):
	return user.has_perm(f"{app_name}.delete_{model_name}")


@register.simple_tag
def get_fields(chl):
	return get_fields_from_cl(chl)


def beutify_field_name(field_name):
	if re.findall(r"__\w+__", field_name).__len__() > 0:
		return field_name

	field_name = field_name.replace("_", " ")
	splitted_ = field_name.split(" ")
	new_name = ""
	for i in splitted_:
		curr_name = i[0].upper()+i[1:]
		new_name += " " + curr_name

	return new_name


@register.simple_tag
def get_all_attributes_of_object(obj, fields=None, chl=None):
	if not fields:
		fields = get_fields_from_cl(chl)
	
	lst = []
	for i in fields:
		lst.append(getattr(obj, i))

	return lst

def make_safe_label(label_tag):
	return label_tag.split("<")[1].split(">")[1]


def cs_list_to_string(lst):
	string = ""
	for i in range(len(lst)):
		if len(lst)-1 == i:
			string += str(lst[i])
		else:
			string += str(lst[i]) + ", "

	return string

def make_month_num_to_string(month_list):
	new_month_string = ""
	for i in range(len(month_list)):
		a = month_list[i]
		if i+1 == len(month_list):
			new_month_string += MONTH_DICT[str(a)]
		else:
			new_month_string += MONTH_DICT[str(a)] + ", "

	return new_month_string


def safe_model_name(model_name):
	breakpoint()
	return model_name


register.filter("beutify_field_name", beutify_field_name)
register.filter("make_safe_label", make_safe_label)
register.filter("list_to_string", cs_list_to_string)
register.filter("make_month_num_to_string", make_month_num_to_string)
register.filter("safe_model_name", safe_model_name)
