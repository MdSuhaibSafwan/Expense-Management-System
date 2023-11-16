from admin_site import admin
from .models import FundHistory


class FundHistoryAdmin(admin.ModelAdmin):
	list_display = ["id", "amount", "title"]


admin.site.register(FundHistory, FundHistoryAdmin)
