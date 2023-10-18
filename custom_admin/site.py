from django.contrib.admin import AdminSite


class MyAdminSite(AdminSite):
    # do some magic
    pass        


site = MyAdminSite()
