# Generated by Django 2.2.7 on 2020-01-30 04:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0007_auto_20200130_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='investment_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='investments.InvestmentClass'),
        ),
    ]
