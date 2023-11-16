import re
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
	help = "To create the groups of Author, Maker, Approver"

	def handle(self, *args, **kwargs):
		self.stdout.write(
			self.style.SUCCESS("Creating Groups of Author, Maker and Approver")
		)
		email = input("Enter Your mail: ")
		password = input("Enter your password: ")
		user = User(email=email, is_staff=True, is_active=True)
		user.set_password(password)
		user.save()
		group = self.create_checker_group()
		user.groups.add(group)
		user.save()

	def get_all_view_permissions(self):
		return Permission.objects.filter(codename__istartswith="view")

	def get_checker_permissions(self):
		view_perms = self.get_all_view_permissions()
		checker_perms_list = ['add_fundcheck','change_fundcheck', 'delete_fundcheck', 'change_fundtransfer']
		perms = Permission.objects.filter(codename__in=checker_perms_list)
		perms |= view_perms
		return perms

	def create_checker_group(self):
		group, created = Group.objects.get_or_create(name="Checker Permission")
		self.stdout.write(
			self.style.SUCCESS("Checker Group Created")
		)
		if created:
			perms = self.get_checker_permissions()
			self.add_perms_to_group(group, perms)

		return group

	def add_perms_to_group(self, group, perms):
	    print("Adding Permissions to Group ", group)
	    self.stdout.write(self.style.SUCCESS("Adding Permissions"))
	    for perm in perms:
	    	group.permissions.add(perm)

	    group.save()
	    return group
