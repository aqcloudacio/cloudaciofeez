# Generated by Django 2.2.7 on 2020-01-30 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0009_auto_20200130_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetallocation',
            name='investment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asset_allocations', to='investments.Investment'),
        ),
    ]
