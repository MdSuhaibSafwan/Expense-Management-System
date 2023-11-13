# Generated by Django 4.2.5 on 2023-10-12 08:39

from django.db import migrations, models
import lib.models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.UUIDField(default=lib.models.create_hex_token, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]