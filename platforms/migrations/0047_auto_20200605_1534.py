# Generated by Django 2.2.7 on 2020-06-05 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0046_auto_20200605_1436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platform',
            old_name='adviser_fee',
            new_name='platform_adviser_fee',
        ),
        migrations.RenameField(
            model_name='platform',
            old_name='adviser_fee_percentage',
            new_name='platform_adviser_fee_percentage',
        ),
    ]