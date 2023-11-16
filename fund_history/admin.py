from admin_site import admin
from .models import FundHistory
from account.models import Account


class FundHistoryAdmin(admin.ModelAdmin):
	change_list_template = "admin/fund_history/fund_history_change.html"
	list_display = ["id", "amount", "title"]

	def changelist_view(self, request, extra_context=None):
		response = super().changelist_view(
			request,
			extra_context=extra_context,
		)

		response.context_data["account_qs"] = Account.objects.all()
		return response


admin.site.register(FundHistory, FundHistoryAdmin)
