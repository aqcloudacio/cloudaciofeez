# Generated by Django 2.2.7 on 2020-03-07 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riskprofiles', '0001_initial'),
        ('users', '0003_remove_user_allowed_portfolios'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='risk_profiles',
            field=models.ManyToManyField(blank=True, related_name='users', to='riskprofiles.RiskProfile'),
        ),
    ]
