# Generated by Django 4.2.5 on 2023-09-17 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_approval_user',
            new_name='is_checker',
        ),
    ]
