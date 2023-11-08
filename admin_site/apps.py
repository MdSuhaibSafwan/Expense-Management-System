from django.apps import AppConfig


def add_perms_to_group(group, perms):
    print("Adding Permissions to Group ", group)


def make_author_group():
    from django.contrib.auth.models import Group
    author_permissions = []
    group, created = Group.objects.get_or_create(name="Author Permission")
    if created:
        add_perms_to_group(group, perms)
    print("Making Author Group")


def make_checker_group():
    from django.contrib.auth.models import Group
    group, created = Group.objects.get_or_create(name="Checker Permission")
    if created:
        add_perms_to_group(group, perms)
    print("Making Checker Group")


def make_approver_group():
    from django.contrib.auth.models import Group
    group, created = Group.objects.get_or_create(name="Approver Permission")
    if created:
        add_perms_to_group(group, perms)
    print("Making Approver Group")


class AdminSiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_site'
    default_site = "admin_site.admin.AdminSiteConfig"

    def ready(self):
        make_author_group()
        make_checker_group()
        make_approver_group()
