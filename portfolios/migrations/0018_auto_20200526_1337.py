# Generated by Django 2.2.7 on 2020-05-26 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0017_auto_20200305_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelinvestment',
            name='investment_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='model_investments', to='investments.InvestmentName'),
        ),
    ]
