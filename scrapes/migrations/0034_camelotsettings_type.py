# Generated by Django 2.2.7 on 2020-08-03 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapes', '0033_camelotsettings_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='camelotsettings',
            name='type',
            field=models.CharField(blank=True, choices=[('aa', 'aa'), ('fee', 'fee'), ('bs', 'bs')], max_length=100, null=True),
        ),
    ]