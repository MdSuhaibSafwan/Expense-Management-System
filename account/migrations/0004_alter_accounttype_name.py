# Generated by Django 4.2.10 on 2024-02-26 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_fundtransfer_transaction_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttype',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
