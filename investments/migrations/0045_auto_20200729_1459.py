# Generated by Django 2.2.7 on 2020-07-29 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0044_auto_20200722_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='investments.InvestmentName'),
        ),
    ]