# Generated by Django 2.2.7 on 2020-01-30 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investments', '0005_investment_investments'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investment',
            old_name='investments',
            new_name='portfolios',
        ),
    ]
