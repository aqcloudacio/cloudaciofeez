# Generated by Django 2.2.7 on 2020-01-30 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0004_remove_portfolio_investments'),
        ('investments', '0004_auto_20200130_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='investments',
            field=models.ManyToManyField(blank=True, related_name='investments', to='portfolios.Portfolio'),
        ),
    ]
