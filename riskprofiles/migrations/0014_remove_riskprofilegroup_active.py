# Generated by Django 2.2.7 on 2020-03-11 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('riskprofiles', '0013_riskprofilegroup_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='riskprofilegroup',
            name='active',
        ),
    ]
