# Generated by Django 2.2.7 on 2020-01-29 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0009_auto_20200129_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformtierpercs',
            name='platform_fee_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tier_percs', to='platforms.PlatformFees'),
        ),
        migrations.AddField(
            model_name='platformtierthresholds',
            name='platform_fee_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tier_thresholds', to='platforms.PlatformFees'),
        ),
    ]
