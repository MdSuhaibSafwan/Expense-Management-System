# Generated by Django 4.2.5 on 2023-10-04 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]