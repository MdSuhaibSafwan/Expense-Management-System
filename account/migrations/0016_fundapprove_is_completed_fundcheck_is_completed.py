# Generated by Django 4.2.5 on 2023-11-08 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_fundapprove_is_2fa_verified_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundapprove',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='fundcheck',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
