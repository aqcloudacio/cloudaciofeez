# Generated by Django 2.2.7 on 2020-03-04 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0016_portfolio_template_id'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='portfolio',
            name='unique_fee_group_default',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='platform_fee_group',
        ),
    ]
