# Generated by Django 2.2.7 on 2020-03-11 02:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riskprofiles', '0009_auto_20200311_1323'),
    ]

    operations = [
        migrations.RenameField(
            model_name='riskprofilegroup',
            old_name='users',
            new_name='allowed_users',
        ),
    ]
