# Generated by Django 4.2.5 on 2023-10-17 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0013_alter_fundtransfer_from_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundcheck',
            name='approver_assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fund_checked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fundtransfer',
            name='checker_assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fund_transfer_checked', to=settings.AUTH_USER_MODEL),
        ),
    ]
