# Generated by Django 2.2.7 on 2020-01-29 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0008_auto_20200129_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platformfees',
            name='tier_percentages',
        ),
        migrations.RemoveField(
            model_name='platformfees',
            name='tier_thresholds',
        ),
    ]