# Generated by Django 4.2.5 on 2023-10-25 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_user2faauth_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user2faauth',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
