# Generated by Django 2.2.7 on 2020-02-10 04:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0017_auto_20200210_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platformfees',
            old_name='admin_fee_dollar',
            new_name='_admin_fee_dollar',
        ),
    ]
