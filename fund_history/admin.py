from admin_site import admin
from .models import FundHistory


class FundHistoryAdmin(admin.ModelAdmin):
	list_display = ["id", "amount", ]


admin.site.register(FundHistory, FundHistoryAdmin)
