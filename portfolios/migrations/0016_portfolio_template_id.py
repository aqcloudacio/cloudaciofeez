# Generated by Django 2.2.7 on 2020-03-04 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0015_portfolio_model_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='template_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]