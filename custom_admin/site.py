from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    # do some magic
    pass        


site = CustomAdminSite()
