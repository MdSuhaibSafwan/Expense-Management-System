# Generated by Django 4.2.5 on 2023-11-08 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0003_alter_category_id_alter_expense_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
