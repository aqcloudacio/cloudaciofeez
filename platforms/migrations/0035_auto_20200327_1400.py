# Generated by Django 2.2.7 on 2020-03-27 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0034_auto_20200326_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='platform_type',
            field=models.CharField(blank=True, choices=[('Accumulation', 'Superannuation - Accumulation'), ('Pension', 'Superannuation - Pension'), ('Defined Benefit', 'Superannuation - Defined Benefit'), ('Investment', 'Investment'), ('SMSF', 'Self Managed Super Fund')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='platform',
            name='status',
            field=models.CharField(blank=True, choices=[('Current', 'Current'), ('Recommended', 'Recommended'), ('Alternative', 'Alternative')], max_length=100, null=True),
        ),
    ]
