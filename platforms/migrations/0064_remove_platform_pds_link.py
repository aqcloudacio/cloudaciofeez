# Generated by Django 2.2.7 on 2020-12-08 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0063_auto_20201124_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platform',
            name='PDS_link',
        ),
    ]
