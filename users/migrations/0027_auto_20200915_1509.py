# Generated by Django 2.2.7 on 2020-09-15 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20200914_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='model_portfolios',
            field=models.ManyToManyField(blank=True, related_name='active_practices', to='portfolios.Portfolio'),
        ),
    ]
