# Generated by Django 2.2.7 on 2020-09-14 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riskprofiles', '0016_auto_20200428_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riskprofilegroup',
            name='AFSL_limitation',
        ),
    ]