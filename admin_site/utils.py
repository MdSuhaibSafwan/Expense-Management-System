from django.contrib.admin.utils import label_for_field


def get_fields_from_cl(chl):
	fields = []
	for i, field_name in enumerate(chl.list_display):
		if field_name == "action_checkbox":
			continue

		text, attr = label_for_field(
			field_name, chl.model, model_admin=chl.model_admin, return_attr=True
		)
		fields.append(field_name)

	return fields