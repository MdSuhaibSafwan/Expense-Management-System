# Generated by Django 4.2.5 on 2023-10-15 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_alter_account_id_alter_accounttype_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fundtransfer',
            name='from_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fund_transfer_from', to='account.account'),
        ),
    ]