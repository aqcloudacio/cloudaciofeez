# Generated by Django 2.2.7 on 2020-01-27 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0003_platformfees'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformTierPercs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.DecimalField(decimal_places=6, max_digits=7)),
            ],
        ),
        migrations.CreateModel(
            name='PlatformTierThresholds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold', models.DecimalField(decimal_places=0, max_digits=7)),
            ],
        ),
        migrations.AddField(
            model_name='platformfees',
            name='tier_percentages',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='non_tier_fees', to='platforms.PlatformTierPercs'),
        ),
        migrations.AddField(
            model_name='platformfees',
            name='tier_thresholds',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='non_tier_fees', to='platforms.PlatformTierThresholds'),
        ),
    ]