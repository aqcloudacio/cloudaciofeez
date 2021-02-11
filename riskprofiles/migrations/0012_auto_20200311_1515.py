# Generated by Django 2.2.7 on 2020-03-11 04:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riskprofiles', '0011_riskprofilegroup_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskprofilegroup',
            name='AFSL_limitation',
            field=models.ManyToManyField(blank=True, related_name='risk_profile_groups', to='users.AFSL'),
        ),
        migrations.AlterField(
            model_name='riskprofilegroup',
            name='allowed_users',
            field=models.ManyToManyField(blank=True, related_name='risk_profile_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
