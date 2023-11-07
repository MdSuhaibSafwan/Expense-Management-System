import re
from django import template
from ..utils import get_fields_from_cl

register = template.Library()


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

register.filter("beutify_field_name", beutify_field_name)
register.filter("make_safe_label", make_safe_label)
register.filter("list_to_string", cs_list_to_string)
