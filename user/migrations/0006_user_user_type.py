# Generated by Django 4.2.5 on 2023-10-04 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_managers_remove_user_is_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[['AU', 'AUTHOR'], ['CH', 'CHECKER'], ['MK', 'MAKER']], max_length=2, null=True),
        ),
    ]
