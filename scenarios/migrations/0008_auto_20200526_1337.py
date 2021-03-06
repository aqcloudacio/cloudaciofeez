# Generated by Django 2.2.7 on 2020-05-26 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scenarios', '0007_scenario_practice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario',
            name='practice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scenarios', to='users.Practice'),
        ),
        migrations.AlterField(
            model_name='scenario',
            name='risk_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scenarios', to='riskprofiles.RiskProfile'),
        ),
    ]
