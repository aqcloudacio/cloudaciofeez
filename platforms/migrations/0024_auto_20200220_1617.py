# Generated by Django 2.2.7 on 2020-02-20 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0023_auto_20200215_1344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platformfees',
            old_name='_admin_fee_dollar',
            new_name='admin_fee_dollar',
        ),
    ]
