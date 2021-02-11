# Generated by Django 2.2.7 on 2020-02-10 05:19

from django.db import migrations, models
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0025_investment_custom_name'),
        ('platforms', '0018_auto_20200210_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformfees',
            name='allowed_investments',
            field=models.ManyToManyField(blank=True, related_name='fee_structures', to='investments.InvestmentName'),
        ),
        migrations.AlterField(
            model_name='platform',
            name='last_checked',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime.now()),
            preserve_default=False,
        ),
    ]
